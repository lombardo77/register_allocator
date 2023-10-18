## register_allocator
Simple bottom up register allocator imnplemented in python. Takes an ILOC program with virtual registers and an integer k, and produces a new ILOC program that uses k physical registers. Works for all testcases in ./testcases directory.


### To run:
```
$ python3 alloc.py [k] [ILOC file name] 
```