from typing import List


def safe_remove(tile: int, tile_set: List[int]) -> bool:
    try:
        tile_set.remove(tile)
        return True
    except ValueError:
        return False


def insert_tile(tile: int, tile_set: List[int]):
    index = 0
    while tile > tile_set[index]:
        index += 1
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
