from src.value_iteration.pickomino_mdp import PickominoMDP
from src.value_iteration.dice_launches import possibleDiceLaunches, launchProbability
from src.value_iteration.state import State

import parameters
import time


def compute_pickomino_or_more_proba(pickomino):
	
	def reward(state,action):
		if state.score >= pickomino and 0 in state.picked and state.stop:
			return 1
		return 0

	return compute_proba_under_reward(pickomino,reward)

def compute_exact_pickomino_proba(pickomino):

	def reward(state,action):
		if state.score == pickomino and 0 in state.picked and state.stop:
			return 1
		return 0

	return compute_proba_under_reward(pickomino,reward)

def compute_proba_under_reward(pickomino,reward):
	tic = time.time()
	mdp.computeOptimalPolicy(reward,resetPolicy=True)
	
	p = 0
	for i in range(len(launchProbability[parameters.NDICES])):
		p += launchProbability[parameters.NDICES][i] * mdp.value[hash(State(possibleDiceLaunches[parameters.NDICES][i],(),0,False))]
	
	return p

mdp = PickominoMDP()

print('Probability of getting a tile with 1 or more pickominos is :',compute_pickomino_or_more_proba(21))
print('Probability of getting a tile with 2 or more pickominos is :',compute_pickomino_or_more_proba(25))
print('Probability of getting a tile with 3 or more pickominos is :',compute_pickomino_or_more_proba(29))
print('Probability of getting a tile with 4 or more pickominos is :',compute_pickomino_or_more_proba(33))


print('Probability of getting exactly tile 24 is',compute_exact_pickomino_proba(24))
print('Probability of getting a tile greater or equal to 27 is :',compute_pickomino_or_more_proba(27))