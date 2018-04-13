from neuromp.preprocessing.tree import AST
from enum import IntEnum, auto
from itertools import product
import subprocess
import time
import numpy as np
from copy import deepcopy

class VarStates(IntEnum):
    SHARED = auto()
    PRIVATE = auto()
    REDUCTION = auto()

class Code(object):
    def __init__(self, code):
        self.ast = AST()
        self.statements = self.ast.parse(code)

        self.lines = self._getLines(code)
        self.for_pos = self.ast.fors[0]
        self.pragmas = self._initPragmas()

        self.best_pragma = self._builtPragma()

        self.seq_time = None
        self.seq_output = None

        self.par_time = None
        self.par_output = None

        self.speed_up = 1.0

        self.max_speed_up = 0.0

        self.actions = list(product(self.ast.variables, list(VarStates)))
        self.runSequential()

    def _getLines(self, code):
        resp = []
        with open(code) as f:
            for l in f:
                l = l.rstrip()
                resp.append(' '.join(l.split()))
        return resp

    def _initPragmas(self):
        resp = {}
        all_vars = self.ast.variables
        for v in all_vars:
            resp[v] = VarStates.SHARED
        return resp

    def _builtPragma(self):
        groups = {}

        resp = "#pragma omp parallel for "

        for k, v in self.pragmas.items():
            if v.name not in groups:
                groups[v.name] = []
            groups[v.name].append(k)

        for k in groups:
            if k == "REDUCTION":
                resp += "{}(+:{}) ".format(k.lower(), ', '.join(groups[k]))
            else:
                resp += "{}({}) ".format(k.lower(), ', '.join(groups[k]))

        return resp.rstrip()

    def getEncodedPragma(self):
        resp = []
        all_vars = self.ast.variables
        for v in all_vars:
            resp.append(12 + self.pragmas[v].value)
        return resp

    def getInput(self):
        resp = self.getEncodedPragma()
        #for s in self.statements:
        #    resp += self.ast.preproStatement(s)
        return np.array(resp)

    def runParallel(self):
        tmp_lines = deepcopy(self.lines)

        tmp_lines.insert(self.for_pos - 1, self._builtPragma())

        with open("tmp_par.c", "w") as f:
            for l in tmp_lines:
                f.write(l + "\n")

        try:
            subprocess.check_output(['gcc-7', '-Wall', '-Werror',
                    '-std=c99', '-O3','-fopenmp', 'tmp_par.c', '-o', 'tmp_par'],
                    stderr=subprocess.STDOUT, universal_newlines=True)
        except subprocess.CalledProcessError as exc:
            self.par_output = None
            self.par_time = 1000
            print("Status : FAIL", exc.returncode, exc.output)
            return self.par_output, self.par_time

        b = time.time()

        p = subprocess.Popen(['./tmp_par'],
                universal_newlines=True,
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE)

        self.par_output, error = p.communicate()
        self.par_time = time.time() - b

        self.par_output = self.par_output.rstrip()

        return self.par_output, self.par_time

    def runSequential(self):
        with open("tmp_seq.c", "w") as f:
            for l in self.lines:
                f.write(l + "\n")

        subprocess.check_output(['gcc-7', '-Wall', '-Werror',
                '-std=c99', '-O3','tmp_seq.c', '-o', 'tmp_seq'],
                stderr=subprocess.STDOUT, universal_newlines=True)

        b = time.time()
        p = subprocess.Popen(['./tmp_seq'],
                universal_newlines=True,
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE)

        self.seq_output, error = p.communicate()
        self.seq_time = time.time() - b

        self.seq_output = self.seq_output.rstrip()

        return self.seq_output, self.seq_time

    def step(self, action):
        a = self.actions[action]
        self.pragmas[a[0]] = a[1]

        reward = self.getReward()
        next_state = self.getInput()
        done = (reward >= self.max_speed_up)

        if done:
            self.max_speed_up = reward
            self.best_pragma = self._builtPragma()

        return next_state, reward, done

    def render(self):
        print(self._builtPragma())

    def speedUp(self):
        return self.seq_time / self.par_time

    def getReward(self):
        self.runParallel()
        if self.seq_output == self.par_output:
            s = self.speedUp()
            if s > 1.0:
                return s
            else:
                return -1
        else:
            return -1

    def reset(self):
        self.pragmas = self._initPragmas()
        return self.getInput()
if __name__ == "__main__":
    c = Code('../data/pi.c')
    print(c.getInput())

    #c.setProperty(8)
    #c.setProperty(10)
    print(c.getInput())

    #print(c.actions)
    print(c.runSequential())
    print(c.runParallel())
    print(c.getReward())
