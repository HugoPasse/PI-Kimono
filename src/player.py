from typing import List
from project_types import ActionType


# Abstract class for Pickomino players
class Player:

    def __init__(self, with_display: bool = False):
        self.with_display = with_display

    def play_round(self, available_tiles: List[int], adversary_tiles: List[int], player_last_tile: int) -> (int, int):
        pass
