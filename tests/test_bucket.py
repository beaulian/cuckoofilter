# coding=utf-8

import pytest
from cuckoofilter.bucket import Bucket, DEFAULT_BUCKET_SIZE

bs = b"test"


@pytest.fixture
def b():
    return Bucket()


def test_size(b):
    assert len(b) == 0


def test_capacity(b):
    assert b.capacity() == DEFAULT_BUCKET_SIZE


def test_insert(b):
    assert b.insert(bs)


def test_insert_type_error(b):
    with pytest.raises(AssertionError) as _:
        b.insert(1)


def test_insert_full(b):
    for i in range(b.capacity()):
        b.insert(bs)
    assert not b.insert(bs)


def test_contains_protocol(b):
    assert bs not in b
    b.insert(bs)
    assert bs in b


def test_delete(b):
    b.insert(bs)
    assert b.delete(bs)
    assert bs not in b


def test_delete_not_exist(b):
    assert not b.delete(bs)


def test_get_fingerprint_index(b):
    assert b.get_fingerprint_index(bs) == -1
    b.insert(bs)
    assert b.get_fingerprint_index(bs) > -1


def test_swap(b):
    bs2 = b"test2"
    b.insert(bs)
    fp, _ = b.swap(bs2)
    assert fp == bs
    assert bs2 in b
