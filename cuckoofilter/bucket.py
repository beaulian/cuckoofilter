# coding=utf-8
import random
import threading

DEFAULT_BUCKET_SIZE = 4


class Bucket(object):

    """A basic cuckoo hash table consists of an array of buckets where each item
       has k candidate buckets determined by k hash functions (k, default to 2)
    """

    def __init__(self):
        self.__capacity = DEFAULT_BUCKET_SIZE
        self.__b = []
        self.__lock = threading.Lock()

    def insert(self, fp):
        """ Insert a fingerprint into bucket, allow duplication

        :param fp: fingerprint
        :return: a bool, insertion fails or succeeds.
        """
        assert isinstance(fp, bytes)

        if len(self.__b) >= self.__capacity:
            return False
        with self.__lock:
            self.__b.append(fp)
        return True

    def delete(self, fp):
        """ Delete a fingerprint from bucket, if the bucket exists
        multiple the same fingerprint, delete the fist one found.

        :param fp: fingerprint
        :return: a bool, deletion fails or succeeds.
        """
        assert isinstance(fp, bytes)

        for i, tfp in enumerate(self.__b):
            if tfp == fp:
                with self.__lock:
                    self.__b.remove(tfp)
                return True
        return False

    def get_fingerprint_index(self, fp):
        """ Get index of fingerprint in bucket

        :param fp: fingerprint
        :return: a int, index of fingerprint, otherwise -1
        """
        try:
            return self.__b.index(fp)
        except ValueError:
            return -1

    def swap(self, fp):
        """ Swap given fingerprint with a random entry stored in the bucket

        :param fp: fingerprint
        :return: a fingerprint, the swapped fingerprint
        """
        i = random.randint(0, len(self) - 1)
        fp, self.__b[i] = self.__b[i], fp
        return fp

    def capacity(self):
        return self.__capacity

    def __contains__(self, fp):
        return self.get_fingerprint_index(fp) > -1

    def __len__(self):
        return len(self.__b)

    def __repr__(self):
        return "<Bucket: capacity=" + str(self.__capacity) + ">"

    def __str__(self):
        return self.__repr__()
