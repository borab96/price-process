import numpy as np


def normalize(vec):
    return vec/np.max(np.abs(vec))


def integer_difference(vec, t, n=1):
    if len(vec) != len(t):
        raise IndexError("lengths of vector and index must match")
    dvec = vec
    for i in range(0, n):
        dvec = np.diff(np.append([dvec[0]], dvec))/abs(t[1]-t[0])
    return dvec
