from pickomino import Pickomino
from player import Player

if __name__ == "__main__":
    player_1 = Player()
    player_2 = Player()
    game = Pickomino(player_1, player_2, with_display=True)
    game.play()

