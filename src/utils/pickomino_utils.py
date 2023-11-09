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


def read_params(file: str) -> (float, float):
    with open(file, 'r') as file:
        last_line = file.readlines()[-1]
        alpha_beta = last_line.split(' ')
        return float(alpha_beta[0]), float(alpha_beta[1])


def write_params(file: str, alpha: float, beta: float, games: int, wins: int):
    with open(file, 'a') as file:
        file.write("\n{} {} {} {}".format(alpha, beta, games, wins))
        return
