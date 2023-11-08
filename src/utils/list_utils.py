import numpy as np
from typing import List


def safe_remove(tile: int, tile_set: List[int]) -> bool:
    try:
        tile_set.remove(tile)
        return True
    except ValueError:
        return False


def insert_tile(tile: int, tile_set: List[int]):
    index = 0
    while index < len(tile_set) and tile > tile_set[index]:
        index += 1
    if index >= len(tile_set):
        tile_set.append(tile)
    else:
        tile_set.insert(index, tile)


def safe_last_tile(tile_set: List[int]) -> int:
    try:
        return tile_set[-1]
    except IndexError:
        return 0


def elements_smaller_than(tile: int, tile_set: List[int]) -> List[int]:
    ret: List[int] = []
    for t in tile_set:
        if t <= tile:
            ret.append(t)
        else:
            break
    return ret


def sorted_arrays(a, b, n):
    # Returns all the sorted arrays of size n
    # with elements in {a,a+1,...,b-1}
    if a == b - 1:
        return np.array([np.ones(n, dtype=np.int16) * a])
    L = []
    for i in range(n + 1):
        head = np.ones(i, dtype=np.int16) * a
        tails = sorted_arrays(a + 1, b, n - i)
        for t in tails:
            L.append(np.concatenate([head, t], axis=0))
    L = np.array(L)
    return L


def biggest_smaller(tile_set: List[int], score: int) -> int:
    biggest = 0
    for tile in tile_set:
        if tile <= score:
            biggest = tile
        else:
            return biggest
    return biggest


def num_sorted_arrays(n, m, L=None):
    '''
    Returns the number of sorted arrays of length n over m elements
    '''
    if not isinstance(L, np.ndarray):
        L = np.full((n + 1, m + 1), -1)

    if (n == 0):
        L[n, m] = 1
        return 1
    if (m <= 0):
        L[n, m] = 0
        return 0

    if L[n - 1, m] == -1:
        num_sorted_arrays(n - 1, m, L)
    if L[n, m - 1] == -1:
        num_sorted_arrays(n, m - 1, L)

    L[n, m] = L[n - 1, m] + L[n, m - 1]
    return L


def sorted_array_index(L, a, b, SortedArrayCount, start=0):
    '''
    Assumes that L is a sorted array with values in {a, a+1, ..., b-1}
    Returns the index in the sequence of sorted lists generated by sorted_arrays(a,b,len(L))
    '''
    n = L.shape[0]
    if start >= n:
        return 0

    return SortedArrayCount[n - start, b - L[start] - 1] + sorted_array_index(L, a, b, SortedArrayCount, start + 1)
