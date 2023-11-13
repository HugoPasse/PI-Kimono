from typing import List

from src import parameters
from src.players.one_turn_player import OneTurnPlayer
from src.utils.pickomino_utils import read_params
from src.value_iteration.pickomino_mdp import PickominoMDP


class SGDPlayer(OneTurnPlayer):

    def __init__(self, alpha=-1, beta=-1, with_display: bool = False, initial_mdp=PickominoMDP()):
        chosen_alpha, chosen_beta = alpha, beta
        if alpha == -1 or beta == -1:
            _, chosen_alpha, chosen_beta = read_params("../../"+parameters.SGD_OUTPUT_FILE)
        super().__init__(chosen_alpha, chosen_beta, with_display, initial_mdp)

    def play_round(self, available_tiles: List[int], adversary_tiles: List[int], player_last_tile: int) -> (int, int):
        return super().play_round(available_tiles, adversary_tiles, player_last_tile)