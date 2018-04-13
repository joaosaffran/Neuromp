import numpy as np
from neuromp.preprocessing.code import Code, VarStates
from itertools import product
class QLearn():
    def __init__(self, env, lr=.8, y=.95, num_episodes=20):
        self.env = env
        self.lr = lr
        self.y = y
        self.num_episodes = num_episodes

        self.states = {}

        self.Q = np.zeros([
                len(list(product(list(VarStates), repeat=len(self.env.ast.variables)))),
                len(env.actions)
                ])

    def get_state_num(self, s):
        aux_s = ''.join([str(c) for c in s])
        if not aux_s in self.states.keys():
            self.states[aux_s] = len(self.states.keys())

        return self.states[aux_s]

    def fit(self):
        rList = []
        for i in range(self.num_episodes):
            s = self.env.reset()
            #print(">> start {}".format(s))
            s = self.get_state_num(s)
            rAll = 0
            d = False

            rEp = []
            epLength = 0

            for j in range(len(self.env.ast.variables)):
                epLength += 1
                a = np.argmax(self.Q[s,:] + np.random.randn(1,len(self.env.actions))*(1./(i+1)))

                s1,r,d = self.env.step(a)
             #   print(s1)
                s1 = self.get_state_num(s1)
                self.Q[s,a] = self.Q[s,a] + self.lr*(r + self.y*np.max(self.Q[s1,:]) - self.Q[s,a])
                rEp.append(r)
                rAll += r
                s = s1
                if d:
                    break
            rList.append(rAll)

            print("{}/{} len: {} glo_avg: {:.2f} max: {:.2f} min:{:.2f} all:{:.2f} ep_avg:{:.2f}".format(
                i,
                self.num_episodes,
                epLength,
                sum(rList)/self.num_episodes,
                max(rEp),
                min(rEp),
                rAll,
                sum(rEp)/len(rEp))
            )
        print(self.Q)
        print(self.env.best_pragma)
if __name__ == "__main__":
    import sys
    q = QLearn(Code(sys.argv[1]))
    print(q.Q.shape)
    q.fit()
