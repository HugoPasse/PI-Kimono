import time
from typing import List
import threading
from src import parameters
from src.pickomino import Pickomino
from src.players.one_turn_player import OneTurnPlayer
from src.utils.pickomino_utils import read_params, write_params


def train_n_steps(n: int, eps=0.0001, step_size=0.001, computer_per_grad=20, verbose=False):
    for i in range(n):
        one_sgd_step(eps, step_size, computer_per_grad)
        print("Iteration: ", i+1)


def one_sgd_step(eps, step_size, nb_compute):
    alpha, beta = read_params("../" + parameters.SGD_OUTPUT_FILE)
    # 0: mean of f(a,b) over nb_compute games
    # 1: mean of f(a+eps, b) over nb_compute games
    # 2: mean of f(a, b+eps) over nb_compute games
    mean_score = [0.0, 0.0, 0.0]
    won = [0, 0, 0]
    lost = [0, 0, 0]
    drew_with_0 = [0, 0, 0]

    alpha_beta_thread = threading.Thread(target=compute_mean, args=(alpha, beta, nb_compute, mean_score, won, lost, drew_with_0, 0))
    dalpha_beta_thread = threading.Thread(target=compute_mean, args=(alpha + eps, beta, nb_compute, mean_score, won, lost, drew_with_0,  1))
    alpha_dbeta_thread = threading.Thread(target=compute_mean, args=(alpha, beta + eps, nb_compute, mean_score, won, lost, drew_with_0,  2))

    alpha_beta_thread.start()
    dalpha_beta_thread.start()
    alpha_dbeta_thread.start()

    alpha_beta_thread.join()
    dalpha_beta_thread.join()
    alpha_dbeta_thread.join()

    gradient = [(mean_score[1] - mean_score[0]) / eps, (mean_score[2] - mean_score[0]) / eps]
    new_alpha = min(max(alpha + gradient[0] * step_size, 0), 2)  # + here we want to maximize score and keep in [0,2]
    new_beta = min(max(beta + gradient[1] * step_size, 0), 2)  # same reason

    total_games_won = won[0] + won[1] + won[2]
    total_games_lost = lost[0] + lost[1] + lost[2]
    total_games_drew_with_0 = drew_with_0[0] + drew_with_0[1] + drew_with_0[2]

    write_params("../" + parameters.SGD_OUTPUT_FILE, new_alpha, new_beta, 3 * nb_compute, total_games_won,
                 total_games_lost, total_games_drew_with_0)


def compute_mean(alpha, beta, nb_compute, mean_score: List[float],
                 games_won: List[int], games_lost: List[int], games_drew_with_0: List[0], index_to_write: int):
    total_points = 0
    won = 0
    lost = 0
    drew_with_0 = 0
    for i in range(nb_compute):
        game = Pickomino(OneTurnPlayer(alpha, beta), OneTurnPlayer())
        pp1, pp2 = game.play()
        total_points += pp1
        if pp1 - pp2 > 0:
            won += 1
        if pp2 - pp1 > 0:
            lost += 1
        if pp1 == pp2 == 0:
            drew_with_0 += 1

    mean_score[index_to_write] = total_points / nb_compute
    games_won[index_to_write] = won
    games_lost[index_to_write] = lost
    games_drew_with_0[index_to_write] = drew_with_0
