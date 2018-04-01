import numpy as np

TYPES = ['double']

ARIT_OPS = [
    "+",
    "-",
    "*",
    "/"
]

ATTR_OPS = [
    "=",
    "+=",
    #"-=",
    #"*="
]

COMP_OPS = [
    ">",
    "<",
    ">=",
    "<="
]

class CodeGen():
    def __init__(self, num_vars=3, num_statements=5):
        self.num_vars = num_vars
        self.num_statements = num_statements
        self.variables = {}

        for _ in range(num_vars):
            self.getVar()

        self.code = self.initVars() + self.genFunc("main", "int", params={"argc": "int", "argv": "char**"})

    def initVars(self):
        inits = []
        for v in self.variables.keys():
            inits.append("%s %s = %s;\n" %(
                self.variables[v],
                v,
                np.random.random() * 100
                ))
        return "".join(inits)

    def getVar(self):
        length = len(self.variables.keys())
        name = "var{}".format(length)
        self.variables[name] = \
                np.random.choice(TYPES, 1)[0]
        return name

    def randVar(self):
        return np.random.choice(list(self.variables.keys()), 1)[0]

    def genFunc(self, name, func_type, params={}):
        params_list = [params[k] + " " + k for k in params.keys()]

        return func_type +' '+name+' ('+\
               ", ".join(params_list)+'){\n'+self.genFor()\
               +'\n printf("%f\\n", '+self.randVar()+');\n}'

    def genFor(self):
        return "for(%s = 0; %s; %s ){\n%s\n}"%("int i", "i<10", "i++", self.genStatements())

    def genStatements(self):
        stmts = []
        for _ in range(self.num_statements):
            stmts.append("%s %s %s;" % (
                self.randVar(),
                np.random.choice(ATTR_OPS, 1)[0],
                self.genAritExpressions()))
        return "\n".join(stmts)

    def genAritExpressions(self, mean=0, std=0.1, threshold=-0.06):

        assert threshold >= -2 * std, "Threshold too low!"

        if np.random.normal(mean, std, 1)[0] > threshold:
            template = "(%s %s %s)"
            if np.random.normal(mean, std, 1)[0] > threshold:
                return template % (self.randVar(),
                        np.random.choice(ARIT_OPS, 1)[0],
                        self.genAritExpressions())
            else:
                return template % (np.random.normal(mean, std, 1)[0] * 10 + 1,
                        np.random.choice(ARIT_OPS, 1)[0],
                        self.genAritExpressions())

        else:
            return self.randVar()


if __name__ == "__main__":
    code = CodeGen()
    print(code.code)
