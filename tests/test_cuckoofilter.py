# coding=utf-8
import pytest
from cuckoofilter import cuckoofilter, bucket

s = "test"


@pytest.fixture
def cf():
    return cuckoofilter.CuckooFilter(capacity=100)


@pytest.fixture
def cf1():
    return cuckoofilter.CuckooFilter(capacity=4)


def test_capacity(cf):
    assert len(cf) == 32


def test_capacity_error():
    with pytest.raises(AssertionError) as _:
        cuckoofilter.CuckooFilter(capacity=1)


def test_insert(cf):
    assert cf.insert(s)
    assert cf.size() == 1


def test_pickle(cf):
    with pytest.raises(cuckoofilter.ItemError) as _:
        cf.insert(pytest)


def test_insert_full(cf):
    for _ in range(bucket.DEFAULT_BUCKET_SIZE << 1):
        cf.insert(s)
    assert not cf.insert(s)


def test_insert_undo(cf1):
    cf1._CuckooFilter__buckets[0]._Bucket__b = [b'1', b'2', b'3', b'4']
    assert not cf1.insert(s)


def test_contains(cf):
    assert not cf.contains(s)
    cf.insert(s)
    assert cf.contains(s)


def test_contains_protocol(cf):
    assert s not in cf
    cf.insert(s)
    assert s in cf


def test_delete(cf):
    cf.insert(s)
    assert cf.delete(s)
    assert not cf.contains(s)


def test_delete_not_exist(cf):
    assert not cf.delete(s)
