from game_player import *
from utils import *
from typing import List
from project_types import ActionType
import os


class Pickomino:

    def __init__(self, first_player: Player, second_player: Player, with_display: bool = False):
        self.with_display = with_display
        self.available_tiles: List[int] = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36]
        self.player_tiles: List[List[int]] = [[], []]
        self.players: List[Player] = [first_player, second_player]

    def play(self):
        player = 0
        adversary = 1
        while len(self.available_tiles) > 0:
            self.display(player, adversary)
            last_tile: int = safe_last_tile(self.player_tiles[player])
            adversary_tiles: List[int] = self.player_tiles[adversary]

            player_action: (int, int) = self.players[player].play_round(self.available_tiles, adversary_tiles,
                                                                        last_tile)
            self.deal_with_action(player, adversary, player_action)
            player, adversary = adversary, player

    def deal_with_action(self, player: int, adversary: int, action: (int, int)):
        action_type, tile = action[0], action[1]

        # If player does not do anything, then they lose their last tile
        if action_type == ActionType.NONE:
            if len(self.player_tiles[player]) > 0:
                last_tile = self.player_tiles[player].pop(-1)
                insert_tile(last_tile, self.available_tiles)

        # If player decides to take a tile, check that it is available and add it to its tiles
        elif action_type == ActionType.TAKE_TILE:
            if safe_remove(tile, self.available_tiles):
                self.player_tiles[player].append(tile)

        # If player decides to steal a tile, check that the adversary has the tile and take it
        elif action_type == ActionType.STEAL_TILE:
            if safe_remove(tile, self.player_tiles[adversary]):
                self.player_tiles.append(tile)

    def display(self, player: int, adversary: int):
        if self.with_display:
            os.system('cls' if os.name == 'nt' else 'clear')
            available_tiles_str = tiles_list_string(self.available_tiles)
            player_tiles_str = tiles_list_string(self.player_tiles[player])
            adversary_tiles_str = tiles_list_string(self.player_tiles[adversary])

            final_string = ("PICKOMINO GAME\n==============\n\n" + "AVAILABLE TILES\n" + available_tiles_str + "\n\n"
                            + "CURRENT PLAYER'S TILES\n" + player_tiles_str + "\n\n" + "ADVERSARY TILES\n"
                            + adversary_tiles_str + "\n\nPlayer " + str(player) + "'s turn to play\n"
                            + "=======================")
            print(final_string)
