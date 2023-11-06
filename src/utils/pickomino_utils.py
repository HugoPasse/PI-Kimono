from typing import List


def tile_value(tile: int) -> int:
    if tile >= 33:
        return 4
    elif tile >= 29:
        return 3
    elif tile >= 25:
        return 2
    elif tile>=21:
        return 1
    else:
        return 0


def total_points(tiles: List[int]) -> int:
    total = 0
    for tile in tiles:
        total += tile_value(tile)
    return total