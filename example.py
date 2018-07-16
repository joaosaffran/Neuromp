from neuromp.model.q_learn import QLearn
from neuromp.preprocessing.code import Code, VarStates

optim = QLearn(Code('./data/pi.c'))
optim.fit()
