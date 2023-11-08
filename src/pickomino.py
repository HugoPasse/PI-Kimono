from src.players.player import *
from src.utils.display_utils import tiles_list_string
from src.utils.list_utils import safe_last_tile, safe_remove, insert_tile

from typing import List
from actions import *
import os

from src.utils.pickomino_utils import total_points
import parameters


class Pickomino:

    def __init__(self,
                 first_player: Player,
                 second_player: Player,
                 with_display: bool = False,
                 available_tiles=None,
                 player_1_tiles=None,
                 player_2_tiles=None,
                 short_end_display=False
                 ):
        self.with_display = with_display
        self.short_end_display = short_end_display
        self.available_tiles: List[int] = parameters.TILES
        self.deleted_tiles: List[int] = []
        self.players_tiles: List[List[int]] = [[], []]
        self.players: List[Player] = [first_player, second_player]

        if available_tiles is not None:
            self.available_tiles = available_tiles

        if player_1_tiles is not None:
            self.players_tiles[0] = player_1_tiles

        if player_2_tiles is not None:
            self.players_tiles[1] = player_2_tiles

    def play(self):
        player = 0
        adversary = 1
        while len(self.available_tiles) > 0:
            self.display(player, adversary)
            last_tile: int = safe_last_tile(self.players_tiles[player])
            adversary_tiles: List[int] = self.players_tiles[adversary]

            player_action: (int, int) = self.players[player].play_round(self.available_tiles, adversary_tiles,
                                                                        last_tile)
            self.deal_with_action(player, adversary, player_action)
            player, adversary = adversary, player
            if self.with_display:
                print("Press anything to pass to next player:")
                input()
        # Compute who won
        player_points = total_points(self.players_tiles[player])
        adversary_points = total_points(self.players_tiles[adversary])
        self.players[player].outcome(adversary_points - player_points)
        self.players[adversary].outcome(player_points - adversary_points)
        player_1_points = player_points if player == 0 else adversary_points
        player_2_points = adversary_points if player == 0 else player_points
        self.end_display(player_1_points, player_2_points)

    def deal_with_action(self, player: int, adversary: int, action: (int, int)):
        action_type, tile = action[0], action[1]

        # If player does not do anything, then they lose their last tile
        if action_type == NONE:
            if len(self.players_tiles[player]) > 0:
                last_tile = self.players_tiles[player].pop()
                insert_tile(last_tile, self.available_tiles)
            self.deleted_tiles.append(self.available_tiles.pop())

        # If player decides to take a tile, check that it is available and add it to its tiles
        elif action_type == PICK_TILE:
            if safe_remove(tile, self.available_tiles):
                self.players_tiles[player].append(tile)

        # If player decides to steal a tile, check that the adversary has the tile and take it
        elif action_type == STEAL_TILE:
            if safe_remove(tile, self.players_tiles[adversary]):
                self.players_tiles[player].append(tile)

    def display(self, player: int, adversary: int, force_show=False):
        if self.with_display or force_show:
            # os.system('cls' if os.name == 'nt' else 'clear')
            available_tiles_str = tiles_list_string(self.available_tiles)
            deleted_tiles_str = tiles_list_string(self.deleted_tiles)
            player_tiles_str = tiles_list_string(self.players_tiles[player])
            adversary_tiles_str = tiles_list_string(self.players_tiles[adversary])

            final_string = ("PICKOMINO GAME\n==============\n\n" + "AVAILABLE TILES\n" + available_tiles_str + "\n\n"
                            + "DELETED TILES\n" + deleted_tiles_str + "\n\n"
                            + "CURRENT PLAYER'S TILES\n" + player_tiles_str + "\n\n" + "ADVERSARY TILES\n"
                            + adversary_tiles_str + "\n\nPlayer " + str(player) + "'s turn to play\n"
                            + "=======================")
            print(final_string)

    def end_display(self, player_1_points: int, player_2_points: int):
        if not self.short_end_display:
            print("Game finished with final state:")
            self.display(0, 1, force_show=True)
        else:
            print("Game ended. Player 1 got {} points. Player 2 got {} points".format(player_1_points, player_2_points))