from src.dice import Dice
from src.players.player import Player
from src.utils.display_utils import *
from src.utils.list_utils import elements_smaller_than
from src.actions import *


def compute_keep(dice: Dice):
    while True:
        print("Which dices do you want to keep?")
        try:
            choice = int(input())
            if choice < 0 or choice > 5:
                print("Please choose a number between 0 and 5!")

            if dice.keep(choice):
                print("You kept dice {} and your score is now {}".format(choice, dice.score))
                return
            else:
                print("Cannot pick dices {}.".format(choice))
        except ValueError:
            print("Please enter a valid integer")
            pass


def continue_throwing(dice: Dice) -> bool:
    if dice.remaining == 0:
        return False

    print("Do you want to continue to roll dices ({} dices remaining)? (y/n)".format(dice.remaining))
    decision = input().lower()
    while decision != "y" and decision != "n":
        print("Read {} with length {}".format(decision, len(decision)))
        print("Please select Y or N. Do you want to continue to roll dices ? (y/n)")
        decision = input().lower()

    return decision == "y"


def pick_tile_input(pickable_tiles: List[int]) -> int:
    pick_tiles_str = str(pickable_tiles)
    while True:
        print("What tile do you want to pick from: " + pick_tiles_str + " ?")
        try:
            choice = int(input())
            if pickable_tiles.count(choice) == 0:
                print("Please pick a tile from the list!")
            else:
                return choice
        except ValueError:
            print("Please enter a valid integer")


def action_choice(score: int, pickable_tiles: List[int]) -> int:
    pick_tiles_str = str(pickable_tiles)
    while True:
        print("Choose an action (enter 1 or 2):\n"
              "1) Pick a tile from available tiles: {}\n"
              "2) Steal the tile with score {}".format(pick_tiles_str, score))
        try:
            choice = int(input())
            if choice != 1 and choice != 2:
                print("Cannot choose an integer different from 1 or 2.")
            elif choice == 1:
                return PICK_TILE
            else:
                return STEAL_TILE

        except ValueError:
            print("Please enter a valid integer")


def strategy_choice(dice: Dice, available_tiles: List[int], adversary_tiles: List[int]) -> (int, int):
    stealable_tile = adversary_tiles.count(dice.score) > 0
    pickable_tiles = elements_smaller_than(dice.score, available_tiles)

    if dice.picked.count(0) == 0:
        print("You haven't picked a worm. Your turns end and you lose your last tile.")
        return NONE, 0
    else:
        if len(pickable_tiles) == 0 and not stealable_tile:
            print("You have no available actions unfortunately!")
            return NONE, 0
        elif not stealable_tile:
            return PICK_TILE, pick_tile_input(pickable_tiles)
        else:
            # In this case the player can choose either to steal a tile or to pick a tile
            action = action_choice(dice.score, pickable_tiles)
            if action == PICK_TILE:
                return PICK_TILE, pick_tile_input(pickable_tiles)
            else:
                return STEAL_TILE, dice.score


class HumanPlayer(Player):

    def __init__(self):
        super().__init__(with_display=True)

    def play_round(self, available_tiles: List[int], adversary_tiles: List[int], player_last_tile: int) -> (int, int):
        dice = Dice()
        dice.print_state()

        # Roll dices
        while True:
            # Check if the player can keep something
            if dice.can_pick():
                compute_keep(dice)
                if not continue_throwing(dice):
                    break
                dice.throw()
                dice.print_state()
            else:
                print("You cannot pick a dice! Your turn has ended and you lose your last tile (if any).")
                return NONE, 0

        # Now make decision with dices
        return strategy_choice(dice, available_tiles, adversary_tiles)

    def outcome(self, has_won: bool, final_nb_of_points: int):
        pass
