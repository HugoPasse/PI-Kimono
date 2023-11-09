import time
from typing import List
import threading
from src import parameters
from src.pickomino import Pickomino
from src.players.one_turn_player import OneTurnPlayer
from src.players.sgd_mdp_player import SGDPlayer
from src.utils.pickomino_utils import read_params, write_params


def one_sgd_step(eps=0.05, step_size=0.05, nb_compute=50, verbose=False):
    alpha, beta = read_params("../"+parameters.SGD_OUTPUT_FILE)
    # 0: mean of f(a,b) over nb_compute games
    # 1: mean of f(a+eps, b) over nb_compute games
    # 2: mean of f(a, b+eps) over nb_compute games
    mean_score = [0, 0, 0]
    won = [0, 0, 0]

    alpha_beta_thread = threading.Thread(target=compute_mean, args=(alpha, beta, nb_compute, mean_score, won, 0))
    dalpha_beta_thread = threading.Thread(target=compute_mean, args=(alpha + eps, beta, nb_compute, mean_score, won, 1))
    alpha_dbeta_thread = threading.Thread(target=compute_mean, args=(alpha, beta + eps, nb_compute, mean_score, won, 2))

    start = time.time()
    alpha_beta_thread.start()
    dalpha_beta_thread.start()
    alpha_dbeta_thread.start()

    alpha_beta_thread.join()
    dalpha_beta_thread.join()
    alpha_dbeta_thread.join()
    compute_time = time.time() - start

    if verbose:
        print("Computed gradient approximation in {} seconds".format(compute_time))

    gradient = [(mean_score[1] - mean_score[0]) / eps, (mean_score[2] - mean_score[0]) / eps]
    new_alpha = alpha + gradient[0] * step_size  # + here we want to maximize score
    new_beta = beta + gradient[1] * step_size  # same reason

    total_games_won = won[0] + won[1] + won[2]

    write_params("../"+parameters.SGD_OUTPUT_FILE, new_alpha, new_beta, 3*nb_compute, total_games_won)


def compute_mean(alpha, beta, nb_compute, mean_score: List[float], games_won: List[int], index_to_write: int):
    total_points = 0
    won = 0
    for i in range(nb_compute):
        print(i)
        game = Pickomino(SGDPlayer(alpha, beta), OneTurnPlayer(), short_end_display=True)
        result = game.play()
        total_points += result
        if result > 0:
            won += 1
    mean_score[index_to_write] = total_points / nb_compute
    games_won[index_to_write] = won
