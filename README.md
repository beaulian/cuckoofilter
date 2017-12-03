cuckoofilter
=====================================================
Cuckoofilter is an implementation of Cuckoo Filter using Python, which is thread-safe.
Besides, the package can both be used in python2.x and python3.x.

Cuckoo Filter
---
Cuckoo filter first appeared in the paper 
[Cuckoo Filter: Practically Better Than Bloom](https://www.cs.cmu.edu/~dga/papers/cuckoo-conext2014.pdf) 
by Bin Fan,David G. Andersen, Michael Kaminsky and Michael D. Mitzenmacher, which is used to
replace Bloom filters for approximate set membership tests. Cuckoo filters support 
adding and removing items dynamically while achieving even higher performance than
Bloom filters. For applications that store many items and target moderately low 
false positive rates, cuckoo filters have lower space overhead than space-optimized 
Bloom filters.

To Know more details of Cuckoo Filter, please read the paper.

Installation
---
Install cuckoofilter using:
```shell
   $ pip install cuckoofilter
```
Or
```shell
   $ pip3 install cuckoofilter
```

Usage
---
```python
    >>> import cuckoofilter
    >>> cf = cuckoofilter.CuckooFilter(capacity=100, fingerprint_size=1)
    
    >>> cf.insert('test')
    66349
    
    >>> cf.contains('test')
    True
    
    >>> cf.delete('test')
    True
```

Testing
---
To test the package and generate a test coverage report, you should run
```shell
   $ pip install pytest coverage pytest-cov
   $ pytest -v -cov=cuckoofilter --cov-report html
```
Or
```shell
   $ pip3 install pytest coverage pytest-cov
   $ python3 -m pytest .
```

License
-------
[GPL-3.0 License](https://github.com/shenaishiren/cuckoofilter/blob/master/LICENSE)