import time

from src.value_iteration.action import Action
from src.value_iteration.dice_launches import possibleDiceLaunches
from src.value_iteration.policy import Policy
from src.value_iteration.state import State

from src.parameters import NDICES


class PickominoMDP:
    def __init__(self, verbose=False):
        self.states = dict()
        self.probabilities = dict()
        self.verbose = verbose
        self.policy = None
        self.init()

    def init(self):
        toVisit = []

        for dices in possibleDiceLaunches[NDICES]:
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
            self.policy.initRandomPolicy(self.states)

        self.value = self.policy.computeValue(reward, self.states, self.probabilities)

        notAFixpoint = True
        while notAFixpoint:
            tic = time.time()
            notAFixpoint = False
            for h in self.states.keys():
                state = self.states[h]
                for a in actions:
                    if not state.isActionLegal(a):
                        pass
                    newVal = self.bellmanStateValue(state, a, reward)
                    if newVal > self.value[h]:
                        self.value[h] = newVal
                        self.policy.d[h] = a
                        notAFixpoint = True
            toc = time.time()

            if self.verbose:
                print('Iteration of value iteration done in', toc - tic, 's')

    def bellmanStateValue(self, state, action, reward):
        s = reward(state, action)
        childProbas = self.probabilities[hash(state)][hash(action)]
        for childHash in childProbas.keys():
            s += childProbas[childHash] * self.value[childHash]
        return s

    def printPolicy(self):
        for h in self.states.keys():
            if not self.policy.d[h] is None:
                print('Val :', self.value[h], '---- Action :', self.policy.d[h].dice, self.policy.d[h].stop, '---- ',
                      end='')
            else:
                print('Val :', self.value[h], '---- Action :', None, None, '---- ', end='')
            self.states[h].printState()


def reward1(state, action):
    if (0 in state.picked) and (state.stop):
        if state.score > 16:
            return 4
        if state.score > 14:
            return 3
        if state.score > 12:
            return 2
        if state.score > 10:
            return 1
    return 0


# action = Action(3, False)

# dices = (0, 1, 3, 3, 3, 4, 4, 5)
# picked = ()
# stop = False


# print('Init')
# tic = time.time()
# mdp = PickominoMDP(verbose=True)
# toc = time.time()
# print('Time elapsed to init MDP:', toc - tic, 's')

# state = State(dices, picked, 0, stop)
# print(mdp.value[hash(state)])