from typing import List

from src import parameters


def value_of(tile: int):
    nb_tiles = len(parameters.TILES)
    first_tile = parameters.TILES[0]
    return min(max(4 * (tile - first_tile) // nb_tiles + 1, 0), 4)


def total_points(tiles: List[int]) -> int:
    total = 0
    for tile in tiles:
        total += value_of(tile)
    return total