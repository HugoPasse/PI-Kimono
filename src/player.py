from project_types import *
from abc import ABC, abstractmethod


# Abstract class for Pickomino players
class Player(ABC):

    def __init__(self, with_display: bool = False):
        self.with_display = with_display

    @abstractmethod
    def play_round(self, available_tiles: list[Tile], adversary_tiles: list[Tile], player_last_tile: Tile) -> Action:
        pass


