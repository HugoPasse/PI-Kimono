from project_types import *


def safe_remove(tile: Tile, tile_set: list[Tile]) -> bool:
    try:
        tile_set.remove(tile)
        return True
    except ValueError:
        return False


def insert_tile(tile: Tile, tile_set: list[Tile]):
    index = 0
    while tile > tile_set[index]:
        index += 1
    tile_set.insert(index, tile)
