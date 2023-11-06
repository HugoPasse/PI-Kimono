from src.value_iteration.action import Action


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