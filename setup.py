# coding=utf-8
from os.path import dirname, join
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

__version__ = '0.0.0.1'
__author__ = 'Jiawen Guan'

with open(join(dirname(__file__), 'README.rst'), 'r') as f:
    readme = f.read()


setup(name='cuckoofilter',
      version=__version__,
      description='Cuckoo Filter implementation using Python',
      long_description=readme,
      author=__author__,
      author_email='jesus.jiawen@gmail.com',
      url='https://github.com/shenaishiren/cuckoofilter',
      license='GPL-3.0',
      packages=['cuckoofilter'],
      install_requires=["mmh3"],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6'
      ],
)