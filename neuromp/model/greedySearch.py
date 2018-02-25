from itertools import product
from neuromp.preprocessing.code import VarStates, Code

class greedySearch():
    def __init__(self, env):
        self.env = env
        self.variables = env.ast.variables
        self.possibilities = product(list(VarStates), repeat=len(self.variables))

def main():
    gs = greedySearch(Code("../data/pi.c"))
    best_pragma = ""
    best_reward = float("-inf")

    for p in gs.possibilities:
        for i, v in enumerate(gs.variables):
            gs.env.pragmas[v] = p[i]
        reward = gs.env.getReward()
        pragma = gs.env._builtPragma()

        if reward > best_reward:
            best_reward = reward
            best_pragma = pragma
        print("{} - {}".format(pragma, reward))

    print(">>> RESULT:\n\t{} - {}".format(best_pragma, best_reward))

if __name__ == "__main__":
    main()
