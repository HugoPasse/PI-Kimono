from typing import List


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
