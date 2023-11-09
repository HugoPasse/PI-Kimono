from pickomino import Pickomino
from src.players.human_player import HumanPlayer
from src.players.one_turn_player import OneTurnPlayer
from src.sgd_trainer import one_sgd_step
from src.value_iteration.pickomino_mdp import PickominoMDP

if __name__ == "__main__":
    # player_1 = HumanPlayer()
    # player_2 = OneTurnPlayer(with_display=True)
    # player_2 = HumanPlayer()
    # print("Initializing MDP")
    # init_mdp = PickominoMDP()
    # player_1 = OneTurnPlayer()
    # player_2 = OneTurnPlayer()
    # game = Pickomino(player_1, player_2, short_end_display=True)
    # game.play()
    one_sgd_step(nb_compute=50, verbose=True)

