from player import *
from utils import safe_remove, insert_tile


class Pickomino:

    def __init__(self, first_player: Player, second_player: Player, with_display: bool = False):
        self.with_display = with_display
        self.available_tiles: list[Tile] = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36]
        self.player_tiles: list[list[Tile]] = [[], []]
        self.players: list[Player] = [first_player, second_player]

    def play(self):
        player = 0
        adversary = 1
        while len(self.available_tiles) > 0:
            last_tile: Tile = self.player_tiles[player][-1]
            adversary_tiles: list[Tile] = self.player_tiles[adversary]

            player_action: Action = self.players[player].play_round(self.available_tiles, adversary_tiles, last_tile)
            self.deal_with_action(player, adversary, player_action)
            player, adversary = adversary, player

    def deal_with_action(self, player: int, adversary: int, last_tile: Tile, action: Action):
        action_type: ActionType = action[0]
        tile: Tile = action[1]

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
