# coding=utf-8
import sys
import mmh3

if sys.version_info[0] == 3:
    from_bytes = lambda b: int.from_bytes(b, "big")
else:
    from_bytes = lambda b: long(b.encode("hex"), 16)


def get_next_pow2(n):
    n -= 1
    n |= n >> 1
    n |= n >> 2
    n |= n >> 4
    n |= n >> 8
    n |= n >> 16
    n |= n >> 32
    n += 1
    return n


get_hash = lambda b: mmh3.hash_bytes(b, 0xdbd342)
