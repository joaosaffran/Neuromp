from sacred import Experiment
from sacred.stflow import LogFileWriter
from sacred.observers import MongoObserver

from neuromp.preprocessing.code import Code
from neuromp.model.greedySearch import GreedySearch

ex = Experiment('Pi Gready Search')
ex.observers.append(MongoObserver.create(
    url='mongodb://joaosaffran:saffran96@ds247648.mlab.com:47648/joaosaffran_tcc',
    db_name='joaosaffran_tcc'))

@ex.config
def config():
    code = '../../data/pi.c'

@ex.automain
@LogFileWriter(ex)
def main(_log, _run, code):

    _log.info("Starting ENV...")
    env = Code(code)
    _log.info("Starting Experiment")

    gs = GreedySearch(env)
    best_pragma = ""
    best_reward = float("-inf")
    best_step = 0

    for j, p in enumerate(gs.possibilities):
        for i, v in enumerate(gs.variables):
            gs.env.pragmas[v] = p[i]

        reward = gs.env.getReward()
        pragma = gs.env._builtPragma()
        _run.log_scalar("training.reward", reward, j)

        if reward > best_reward:
            best_reward = reward
            best_pragma = pragma
            best_step = j

        _log.info("{} - {} ({})".format(pragma, reward, j))

    _log.info(">>> RESULT:\n\t{} - {} ({})".format(best_pragma, best_reward, best_step))

    return "{} - {} ({})".format(best_pragma, best_reward, best_step)
