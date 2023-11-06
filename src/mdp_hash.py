import time
import random
import numpy as np

from src.utils.list_utils import sorted_arrays, num_sorted_arrays, sorted_array_index
from src.utils.proba_utils import pascal_triangle, proba_of_list

possibleDiceLaunches = [[]] + [sorted_arrays(0, 6, i) for i in range(1, 9)]
pascalTriangle = pascal_triangle(9)
launchProbability = []

for i in range(len(possibleDiceLaunches)):
    launchProbability.append([])
    for j in range(len(possibleDiceLaunches[i])):
        launchProbability[i].append(proba_of_list(possibleDiceLaunches[i][j], pascalTriangle))
        possibleDiceLaunches[i][j] = tuple(possibleDiceLaunches[i][j])


class Action:
    def __init__(self, dice, stop):
        self.dice = dice
        self.stop = stop

    def __hash__(self):
        return self.dice + 6 * self.stop

    def __eq__(self, other):
        return self.dice == other.dice and self.stop == other.stop


class State:
    def __init__(self, dices, picked, score, stop, verbose=False):
        self.dices = tuple(dices)
        self.score = score
        self.picked = frozenset(picked)
        self.stop = stop

    def isActionLegal(self, action):
        return (not action.dice in self.picked) and (action.dice in self.dices)

    def nextStatesUnderAction(self, action):
        if self.isActionLegal(action):
            L = []
            P = []

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
                L.append(State(dices, newPicked, newScore, action.stop))
                P.append(launchProbability[rem][i])
            return L, P
        return ([], [])

    def nextStates(self):
        actions = [Action(i, False) for i in range(6)] + [Action(i, True) for i in range(6)]
        self.childrenStates = []
        for action in actions:
            self.childrenStates.append(self.nextStatesUnderAction(action))
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


class Policy:
    def __init__(self):
        self.d = dict()
        self.actions = [Action(i, False) for i in range(6)] + [Action(i, True) for i in range(6)]

    def initRandomPolicy(self, states, probabilities):
        t = 0
        for h in states.keys():  # Iterate over states
            st = states[h]
            self.d[h] = None
            for a in range(12):  # Find an action that can be performed
                if len(probabilities[h][a]) > 0:
                    for g in probabilities[h][a].keys():  # Find a state that can be reached from st by doing action ai
                        nextState = states[g]
                        break
                    self.d[h] = self.actions[a]
                    break

    def computeValue(self, reward, states, probabilities):
        self.value = dict()
        for h in states.keys():
            if not (h in self.value):
                self.stateValue(h, reward, states, probabilities)
        return self.value

    def stateValue(self, h, reward, states, probabilities):
        state = states[h]
        action = self.d[h]

        if action is None:
            self.value[h] = reward(state, action)
            return 0

        childProbas = probabilities[h][hash(action)]
        s = reward(state, action)
        if s != 0:
            print('s = ', s, 'for state :', end='')
            state.printState()

        for childHash in childProbas.keys():
            if not (childHash in self.value):
                self.stateValue(childHash, reward, states, probabilities)
            s += self.value[childHash] * childProbas[childHash]

        self.value[h] = s


class PickominoMDP:
    def __init__(self, verbose=False):
        self.states = dict()
        self.probabilities = dict()
        self.verbose = verbose
        self.policy = None

        self.init()

    def init(self):
        toVisit = []

        for dices in possibleDiceLaunches[8]:
            state = State(dices, [], 0, False)
            toVisit.append(state)
            self.states[hash(state)] = state
            self.probabilities[hash(state)] = dict()

        while len(toVisit) > 0:
            state = toVisit.pop()
            childrenStates = state.nextStates()
            self.probabilities[hash(state)] = []

            for a, sublist in enumerate(childrenStates):
                b = True
                self.probabilities[hash(state)].append(dict())
                for i in range(len(sublist[0])):
                    st = sublist[0][i]
                    prob = sublist[1][i]
                    if b:
                        if not hash(st) in self.states.keys():
                            toVisit.append(st)
                            self.states[hash(st)] = st
                            self.probabilities[hash(st)] = []
                        else:
                            b = False

                    self.probabilities[hash(state)][a][hash(st)] = prob

        if self.verbose: print('Accessible states :', len(self.states))

    def computeOptimalPolicy(self, reward, resetPolicy=False):
        '''
		Reward is a function State x Action -> R
		If s is specified we compute the optimal policy starting from s
		'''
        actions = [Action(i, False) for i in range(6)] + [Action(i, True) for i in range(6)]
        if (resetPolicy) or (self.policy is None):
            self.policy = Policy()
            self.policy.initRandomPolicy(self.states, self.probabilities)

        self.value = self.policy.computeValue(reward, self.states, self.probabilities)

        notAFixpoint = True
        while notAFixpoint:
            tic = time.time()
            notAFixpoint = False
            for h in self.states.keys():
                state = self.states[h]
                for a in actions:
                    newVal = self.bellmanStateValue(state, a, reward)
                    if newVal > self.value[h]:
                        self.value[h] = newVal
                        self.policy.d[h] = a
                        notAFixpoint = True
            toc = time.time()
            s = 0
            for i in self.value.values():
                s += i ** 2
            print('Iteration of value iteration done in', toc - tic, 's', s ** 0.5)

        for h in self.states.keys():
            if not self.policy.d[h] is None and self.verbose:
                print('Val :', self.value[h], '---- Action :', self.policy.d[h].dice, self.policy.d[h].stop, '---- ',
                      end='')
            else:
                if self.verbose:
                    print('Val :', self.value[h], '---- Action :', None, None, '---- ', end='')
            if self.verbose:
                self.states[h].printState()

    def bellmanStateValue(self, state, action, reward):
        s = reward(state, action)
        h = hash(state)
        childProbas = self.probabilities[h][hash(action)]

        for childHash in childProbas.keys():
            if childHash in self.value:
                s += childProbas[childHash] * self.value[childHash]
            else:
                print('Cannot properly compute the Bellman value of', h, 'because node', childHash, 'is not inited')
        return s


def reward1(state, action):
    if (0 in state.picked) and (state.stop):
        if state.score <= 37:
            if state.score > 32:
                return 4
            if state.score > 28:
                return 3
            if state.score > 24:
                return 2
            if state.score > 20:
                return 1
    return 0

# action = Action(3, False)

# dices = (3, 3, 5, 5)
# picked = [1, 2]
# stop = False

# state = State(dices, picked, 12, stop)

# tic = time.time()
# mdp = PickominoMDP(verbose=True)
# toc = time.time()
# print('Time elapsed to init MDP:', toc - tic, 's')

# mdp.computeOptimalPolicy(reward1)
