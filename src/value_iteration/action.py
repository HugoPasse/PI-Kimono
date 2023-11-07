class Action:
    def __init__(self, dice, stop):
        self.dice = dice
        self.stop = stop

    def __hash__(self):
        return self.dice + 6 * self.stop

    def __eq__(self, other):
        return self.dice == other.dice and self.stop == other.stop