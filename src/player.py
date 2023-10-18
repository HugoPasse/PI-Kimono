'''
Game classes
'''
import numpy as np

class dice_launcher:
	def __init__(self,verbose = False):
		self.dices = np.random.randint(6,size=8	,dtype=np.int16)
		self.picked = np.zeros(6,dtype=np.int16)
		self.score = 0
		self.remaining = 8
		self.verbose = verbose

	def keep(self,i):
		if self.picked[i] == 1 or np.where(self.dices == i)[0].size == 0:
			if self.verbose : print('Can\'t pick',i)
			return -1
		self.picked[i] = 1

		count = np.count_nonzero(self.dices == i)
		self.remaining -= count

		if i == 0:
			self.score += 5 * count
		else:
			self.score += i * count
		return 0
	
	def stop(self):
		if self.picked[0] == 1:
			return score
		return -1

	def throw(self):
		# Check if it is legal to throw
		if self.remaining < self.dices.size:
			self.dices = np.random.randint(6,size=self.remaining,dtype=np.int16)
		if self.verbose : print('Can\'t throw again, pick a set of dices before')
		return -1

	def print_state(self):
		print('Dices :',self.dices)
		print('Score :',self.score)
		print('Taken :',np.argwhere(self.picked == 1).flatten())
		print('Remainnig :', self.remaining)
		print('')