from typing import List


def safe_remove(tile: int, tile_set: List[int]) -> bool:
    try:
        tile_set.remove(tile)
        return True
    except ValueError:
        return False


def insert_tile(tile: int, tile_set: List[int]):
    index = 1
    while tile > tile_set[index - 1]:
        index += 1
    tile_set.insert(index, tile)


def safe_last_tile(tile_set: List[int]) -> int:
    try:
        return tile_set[-1]
    except IndexError:
        return 0


def tiles_list_string(tiles: List[int]):
    if len(tiles) == 0:
        return ""
    else:
        first_line = "╔"
        second_line = "║"
        third_line = "╚"
        for tile in tiles:
            first_line += "════╦"
            second_line += " {} ║".format(tile)
            third_line += "════╩"
        first_line = first_line[:-1] + "╗"
        third_line = third_line[:-1] + "╝"

    final = first_line + "\n" + second_line + "\n" + third_line
    return final
