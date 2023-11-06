"""
Game classes
"""
import numpy as np


class Dice:
    def __init__(self, verbose=False):
        self.dices = np.random.randint(6, size=8, dtype=np.int16)
        self.dices.sort()
        self.picked = []
        self.score = 0
        self.remaining = 8
        self.verbose = verbose

    def keep(self, i) -> bool:
        if (i in self.picked) or (np.where(self.dices == i)[0].size == 0):
            if self.verbose: print('Can\'t pick', i)
            return False

        self.picked.append(i)

        count = np.count_nonzero(self.dices == i)
        self.remaining -= count

        if i == 0:
            self.score += 5 * count
        else:
            self.score += i * count
        return True

    def stop(self):
        if 0 in self.picked:
            return self.score
        return -1

    def throw(self):
        # Check if it is legal to throw
        if self.remaining < self.dices.size:
            self.dices = np.random.randint(6, size=self.remaining, dtype=np.int16)
            self.dices.sort()
        if self.verbose: print('Can\'t throw again, pick a set of dices before')
        return -1

    def print_state(self):
        print('Score :', self.score)
        print('Taken :', self.picked)
        print('Remaining :', self.remaining)
        print('Dices :', self.dices)
        print('')

    def can_pick(self) -> bool:
        for dice in self.dices:
            if not dice in self.picked:
                return True

        return False
