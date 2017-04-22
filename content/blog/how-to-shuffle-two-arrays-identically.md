+++
Tags = ["numpy","cookbook","python"]
Description = ""
date = "2017-01-20T17:24:40+01:00"
title = "How to shuffle two arrays to the same order"

+++

This is a small recipe on how to get two arrays with the same shape (same
length) shuffled with the same "random seed". This is useful when the two
arrays hold related data (for example, one holds values and the other one holds
labels for those values).

It takes advantage of the fact that numpy arrays can be indexed with other
arrays, something that seems really magical when compared to regular python
arrays.

```
>>> import numpy as np
>>> x = np.arange(10)
>>> y = np.arange(9, -1, -1)
>>> x
array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
>>> y
array([9, 8, 7, 6, 5, 4, 3, 2, 1, 0])
>>> s = np.arange(x.shape[0])
>>> np.random.shuffle(s)
>>> s
array([9, 3, 5, 2, 6, 0, 8, 1, 4, 7])
>>> x[s]
array([9, 3, 5, 2, 6, 0, 8, 1, 4, 7])
>>> y[s]
array([0, 6, 4, 7, 3, 9, 1, 8, 5, 2])
```
