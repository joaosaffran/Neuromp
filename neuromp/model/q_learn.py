import numpy as np
from neuromp.preprocessing.code import Code, VarStates
from itertools import product
from multiprocessing import cpu_count

import time

class QLearn():
    def __init__(self, env, lr=.8, y=.95, num_episodes=1000, early_stop_min_speedup=0.8):
        self.env = env
        self.lr = lr
        self.y = y
        self.num_episodes = num_episodes

        self.early_stop_min_speedup = cpu_count() * early_stop_min_speedup

        self.states = {}
        self.train_info = []
        print(list(VarStates))
        print(env.actions)
        self.exec_time = 0.0
        self.Q = np.zeros([
                len(list(product(list(VarStates), repeat=len(self.env.ast.variables)))),
                len(env.actions)
                ])

    def get_state_num(self, s):
        aux_s = ''.join([str(c) for c in s])
        if not aux_s in self.states.keys():
            self.states[aux_s] = len(self.states.keys())

        return self.states[aux_s]

    def fit(self, ealy_stop_count=5):
        rList = []
        last_mean_speedup = 0
        stopped = ealy_stop_count

        begin = time.time()
        for i in range(self.num_episodes):
            s = self.env.reset()
            #print(">> start {}".format(s))
            s = self.get_state_num(s)
            rAll = 0
            d = False

            rEp = []
            epLength = 0

            for j in range(10 * len(self.env.ast.variables)):
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

            mean_speedup = sum(rEp)/len(rEp)

            aux_tupple = (
                i,
                self.num_episodes,
                epLength,
                sum(rList)/self.num_episodes,
                max(rEp),
                min(rEp),
                rAll,
                mean_speedup)
            self.train_info.append(aux_tupple)

            if last_mean_speedup > 1.0\
                    and mean_speedup > 1.0\
                    and epLength == len(self.env.ast.variables):

                stopped -= 1
                if stopped == 0:
                    break
            else:
                stopped = ealy_stop_count

            last_mean_speedup = mean_speedup
            print("{}/{} len: {} glo_avg: {:.2f} max: {:.2f} min:{:.2f} all:{:.2f} ep_avg:{:.2f} stopped: {}".format(
                i,
                self.num_episodes,
                epLength,
                sum(rList)/self.num_episodes,
                max(rEp),
                min(rEp),
                rAll,
                sum(rEp)/len(rEp),
                stopped)
            )
        all_time = time.time() - begin
        self.exec_time = all_time - self.env.total_time

        print("Total Execution time: {}".format(all_time))
        print("Q-Learning time: {}".format(self.exec_time))
        print("Code Execution time: {}".format(self.env.total_time))

#        print(self.Q)

        print(self.env.best_pragma)
if __name__ == "__main__":
    import sys
    q = QLearn(Code(sys.argv[1]))
    print(q.Q.shape)
    q.fit()
