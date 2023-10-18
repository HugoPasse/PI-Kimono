"""
Utility functions
Some of them will probably be useless
"""

import numpy as np


def pascal_triangle(n):
    # Returns the pascal triangle, T[n,k] is n choose k
    T = np.zeros((n + 1, n + 1), dtype=np.int64)
    T[0, 0] = 1
    for i in range(1, n + 1):
        T[i, 0] = 1
        T[i, i] = 1
        for j in range(1, i):
            T[i, j] = T[i - 1, j - 1] + T[i - 1, j]
    return T


def compute_dice_probabilities(n, faces=6):
    # Returns P such that P[n,k] is the probabilty of having
    # exactly k dices out of n at the same (given) value
    P = np.zeros((n + 1, n + 1))
    r = 1 / faces
    Binom = pascal_triangle(n)
    for i in range(n + 1):
        for j in range(i + 1):
            if Binom[i, j] != 0:
                P[i, j] = (r ** j) * ((5 * r) ** (i - j)) * Binom[i, j]
    return P


def proba_of_list(l, tri):
    """
    Computes the probability of a die launch to be the sorted array l.
    :param l: numpy array (not a list)
    :param tri: the pascal triangle, should be computed up to rank len(l)
    :return:
    """
    choices = 1
    n = len(l)
    for k in range(0, max(l) + 1):
        choices *= tri[n, np.count_nonzero(l == k)]
    return (1 / 6) ** n * choices
