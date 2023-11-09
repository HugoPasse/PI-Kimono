from typing import List, Callable

from src import parameters
from src.actions import LOSE_TILE, PICK_TILE, STEAL_TILE
from src.dice import Dice
from src.players.player import Player
from src.utils.list_utils import biggest_smaller
from src.utils.pickomino_utils import value_of
from src.value_iteration.action import Action
from src.value_iteration.pickomino_mdp import PickominoMDP
from src.value_iteration.state import State


class OneTurnPlayer(Player):

    def __init__(self, alpha: float = 1, beta: float = 1, with_display: bool = False, initial_mdp=PickominoMDP()):
        super().__init__(with_display)
        self.alpha = alpha
        self.beta = beta
        if with_display:
            print("Initializing one turn MDP player")

        self.mdp = initial_mdp

    def tile_decision(self, available_tiles: List[int], adversary_tiles: List[int], player_last_tile, state: State) -> (
            float, int, int):
        """
        Returns the decision taken by an (alpha, beta) player after drawing dices. The final decision always maximizes
        the maximum difference between the player's points and the opponent's weighted with alpha and beta factors.
        In case stealing the opponent's tile is as valuable as picking a tile, the player decides to steal the opponent's
        tile.
        :param available_tiles: tiles that the player can pick.
        :param adversary_tiles: opponent's tiles.
        :param player_last_tile: last tile that the player got (the one they can lose).
        :param state: state of the turn.
        :return: triple (score, tile action, tile to pick)
        """
        if state is not None and state.stop:
            if 0 in state.picked:
                tile_to_pick = biggest_smaller(available_tiles, state.score)
                steal_score = 0
                pick_score = value_of(tile_to_pick)
                if state.score in adversary_tiles:
                    steal_score = self.beta * 2 * value_of(state.score)

                if steal_score == 0 and pick_score == 0:
                    return -self.alpha * value_of(player_last_tile), LOSE_TILE, player_last_tile
                else:
                    if pick_score > steal_score:
                        return pick_score, PICK_TILE, tile_to_pick
                    else:
                        return steal_score, STEAL_TILE, state.score
            else:
                return -self.alpha * value_of(player_last_tile), LOSE_TILE, player_last_tile
        else:
            return 0, LOSE_TILE, 0

    def reward(self, available_tiles: List[int], adversary_tiles: List[int], player_last_tile: int,
               state: State) -> float:
        reward, _, _ = self.tile_decision(available_tiles, adversary_tiles, player_last_tile, state)
        return reward

    def play_round(self, available_tiles: List[int], adversary_tiles: List[int], player_last_tile: int) -> (int, int):
        round_reward: Callable[[State, Action], float] = lambda state, action: (
            self.reward(available_tiles, adversary_tiles, player_last_tile, state))
        if self.with_display:
            print("Computing optimal policy (this can take time)...")
        reward_string = ""
        for i in range(parameters.NDICES * 5):
            state = State([], [0], i, True)
            action = Action([], True)
            reward_string += str(round_reward(state, action)) + " "
        # print(reward_string)
        self.mdp.computeOptimalPolicy(round_reward, resetPolicy=True)

        policy = self.mdp.policy
        dice = Dice()
        state = State(dice.dices, frozenset([]), 0, False)
        boucles_nb = 0
        while not state.stop:
            boucles_nb += 1

            if self.with_display:
                dice.print_state()
            action = policy.d[hash(state)]

            if action is None:
                break

            if boucles_nb >= parameters.NDICES + 2:
                print(
                    "{} boucles faites. Action : {} {}. State: {} {} {} {}".format(boucles_nb, action.dice, action.stop,
                                                                                   state.dices, state.picked,
                                                                                   state.score, state.stop))
                return LOSE_TILE, player_last_tile

            dice.keep(action.dice)

            if self.with_display:
                print("Computer decided to keep dice {}\n\n".format(action.dice))

            dice.throw()
            state = State(dice.dices, dice.picked, dice.score, action.stop)
            if action.stop:
                break

        _, tile_action, tile_tile = self.tile_decision(available_tiles, adversary_tiles, player_last_tile, state)
        if self.with_display:
            if tile_action == LOSE_TILE:
                print("Computer could not take an action and lost tile {}".format(tile_tile))
            elif tile_action == STEAL_TILE:
                print("Computer decided to steal your tile {}".format(tile_tile))
            else:
                print("Computer decided to pick tile {}".format(tile_tile))
        return tile_action, tile_tile
