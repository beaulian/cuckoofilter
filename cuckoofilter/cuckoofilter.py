# coding=utf-8

import random
import threading
from . import bucket
from .utils import get_next_pow2, get_hash, from_bytes

try:
    import cPickle as pickle
except ImportError:
    import pickle

MAX_CUCKOO_COUNT = 500


class ItemError(Exception):
    pass


class CuckooFilter(object):
    """
    A new data structure that can replace Bloom filters
    for approximate set membership tests. Cuckoo filters
    support adding and removing items dynamically while
    achieving even higher performance than Bloom filters.
    For applications that store many items and target
    moderately low false positive rates, cuckoo filters
    have lower space overhead than space-optimized Bloom filters
    """

    def __init__(self, capacity, fingerprint_size=1):
        """Initialize `CuckooFilter` class

        :param capacity: buckets' number in cuckoofilter
        :param fingerprint_size: size of the fingerprint in bytes
               the larger fingerprint size is, the lower false positive
               rates are.
        """
        self.__capacity = int(get_next_pow2(capacity) / bucket.DEFAULT_BUCKET_SIZE)
        self.__fingerprint_size = fingerprint_size
        self.__count = 0   # record the number of fingerprints in cuckoofilter
        self.__buckets = [bucket.Bucket() for _ in range(self.__capacity)]
        self.__lock = threading.Lock()

    def insert(self, item):
        """Insert a item to cuckoofilter

        :param item: determined by user, must be serializable
        :return: a bool, insertion fails or succeeds
        """
        fp, i1, i2 = self._get_fingerprint_and_index_pair(item)
        if self._insert(fp, i1) or self._insert(fp, i2):
            return True

        # reinsert, kick out some fps
        i = random.choice([i1, i2])
        for k in range(MAX_CUCKOO_COUNT):
            # swap
            fp = self.__buckets[i].swap(fp)
            i = self._get_alter_index(fp, i)
            if self._insert(fp, i):
                return True
        return False

    def _insert(self, fp, i):
        if self.__buckets[i].insert(fp):
            # increase counter
            with self.__lock:
                self.__count += 1
            return True
        return False

    def _get_fingerprint_and_index_pair(self, item):
        # f = fingerprint(x)
        # i1 = hash(x)
        # i2 = i1 ^ hash(f)
        try:
            item = pickle.dumps(item)
        except TypeError:
            raise ItemError("item %s is not serializable" % str(item))

        hash_ = get_hash(item)
        fp = hash_[:self.__fingerprint_size]
        i1 = from_bytes(hash_) % self.__capacity
        i2 = self._get_alter_index(fp, i1)
        return fp, i1, i2

    def _get_alter_index(self, fp, i):
        return (i ^ from_bytes(get_hash(fp))) % self.__capacity

    def delete(self, item):
        """Delete a item from cuckoofilter

        :param item: determined by user, must be serializable
        :return: a bool, deletion fails or succeeds
        """
        fp, i1, i2 = self._get_fingerprint_and_index_pair(item)
        return self._delete(fp, i1) or self._delete(fp, i2)

    def _delete(self, fp, i):
        if self.__buckets[i].delete(fp):
            with self.__lock:
                self.__count -= 1
            return True
        return False

    def contains(self, item):
        """Lookup whether item is in cuckoofilter or not

        :param item: determined by user, must be serializable
        :return: a bool, in or not in
        """
        fp, i1, i2 = self._get_fingerprint_and_index_pair(item)
        b1, b2 = self.__buckets[i1], self.__buckets[i2]
        return (b1.get_fingerprint_index(fp) > -1) or (b2.get_fingerprint_index(fp) > -1)

    def capacity(self):
        return self.__capacity

    def size(self):
        return self.__count

    def __contains__(self, item):
        return self.contains(item)

    def __len__(self):
        return self.__capacity

    def __repr__(self):
        return "<CuckooFilter: capacity=" + str(self.__capacity) + \
               ", fingerprint_size=" + str(self.__fingerprint_size) + ' byte(s)>'

    def __str__(self):
        return self.__repr__()
