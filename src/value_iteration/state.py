from src.value_iteration.action import Action
from src.value_iteration.dice_launches import possibleDiceLaunches, launchProbability


class State:
    def __init__(self, dices, picked, score, stop, verbose=False):
        self.dices = tuple(dices)
        self.score = score
        self.picked = frozenset(picked)
        self.stop = stop

    def isActionLegal(self, action):
        return (action.dice not in self.picked) and (action.dice in self.dices)

    def nextStatesUnderAction(self, action):
        if self.isActionLegal(action):
            L = ()
            P = ()

            count = self.dices.count(action.dice)
            val = action.dice + 5 * (action.dice == 0)

            newScore = self.score + count * val

            if action.stop:
                newPicked = []
                if 0 in self.picked or action.dice == 0:
                    newPicked.append(0)
                return [State(frozenset([]), frozenset(newPicked), newScore, True)], [1]

            newPicked = frozenset.union(self.picked, frozenset([action.dice]))
            rem = len(self.dices) - count

            for i, dices in enumerate(possibleDiceLaunches[rem]):
                L += (State(dices, newPicked, newScore, action.stop),)
                P += (launchProbability[rem][i],)
            return (L, P)
        return ((), ())

    def nextStates(self):
        actions = [Action(i, False) for i in range(6)] + [Action(i, True) for i in range(6)]
        self.childrenStates = ()
        for action in actions:
            self.childrenStates += (self.nextStatesUnderAction(action),)
        return self.childrenStates

    def printState(self):
        if self.stop:
            print('Final state with score :', self.score)
        else:
            print('Dices :', self.dices, '| already picked dices :', tuple(self.picked), '| score :', self.score)

    def __hash__(self):
        return hash((self.dices, self.score, self.picked, self.stop))

    def __eq__(self, other):
        return self.dices == other.dices and self.picked == other.picked and self.score == other.score and self.stop == other.score
