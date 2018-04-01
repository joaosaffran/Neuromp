from itertools import product
from neuromp.preprocessing.code import VarStates

class GreedySearch():
    def __init__(self, env):
        self.env = env
        self.variables = env.ast.variables
        self.possibilities = product(list(VarStates), repeat=len(self.variables))
