import time

from pickomino import Pickomino
from src.players.human_player import HumanPlayer
from src.players.one_turn_player import OneTurnPlayer
from src.sgd_trainer import one_sgd_step, train_n_steps
from src.value_iteration.pickomino_mdp import PickominoMDP

if __name__ == "__main__":
    # player_1 = HumanPlayer()
    # player_2 = OneTurnPlayer(with_display=True)
    # player_2 = HumanPlayer()
    # print("Initializing MDP")
    # init_mdp = PickominoMDP()
    start = time.time()
    train_n_steps(1)
    total_time = time.time() - start
    print(total_time)


