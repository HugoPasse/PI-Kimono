import time

from src.value_iteration.action import Action
from src.value_iteration.dice_launches import possibleDiceLaunches
from src.value_iteration.policy import Policy
from src.value_iteration.state import State


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

        if self.verbose:
            print('Accessible states :', len(self.states))

    def computeOptimalPolicy(self, reward, resetPolicy=False):
        """
        Reward is a function State x Action -> R
        If s is specified we compute the optimal policy starting from s
        """

        actions = [Action(i, False) for i in range(6)] + [Action(i, True) for i in range(6)]
        if resetPolicy or (self.policy is None):
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
