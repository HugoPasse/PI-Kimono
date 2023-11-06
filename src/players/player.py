from typing import List


# Abstract class for Pickomino players
class Player:

    def __init__(self, with_display: bool = False):
        self.with_display = with_display

    def play_round(self, available_tiles: List[int], adversary_tiles: List[int], player_last_tile: int) -> (int, int):
        """
        Plays a single round of Pickomino(without cheating) from the state of the game.
        :param available_tiles: tiles that the player can pick.
        :param adversary_tiles: tiles that the player can steal from the adversary.
        :param player_last_tile: last tile that the player got (0 if none).
        :return: the pair (action, tile), where action is NONE, PICK_TILE OR STEAL_TILE and tile is the associated tile
                 number.
        """
        pass

    def outcome(self, has_won: bool, final_nb_of_points: int):
        """
        Called by the Pickomino game has ended to tell if the player has won and how much points they scored
        """
        pass
