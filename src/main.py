import time

from pickomino import Pickomino
from src.players.human_player import HumanPlayer
from src.players.one_turn_player import OneTurnPlayer
from src.players.sgd_player import SGDPlayer

if __name__ == "__main__":
    player_1 = HumanPlayer()
    player_2 = OneTurnPlayer(with_display=True)
    player_3 = SGDPlayer(with_display=True)
    game = Pickomino(player_1, player_2, with_display=True)
    game.play()




