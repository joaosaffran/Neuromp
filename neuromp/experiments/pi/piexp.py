from sacred import Experiment
from sacred.stflow import LogFileWriter
from sacred.observers import MongoObserver

from neuromp.preprocessing.code import Code
from neuromp.model.model import QNet
import numpy as np
import tensorflow as tf

ex = Experiment('Running Pi')
ex.observers.append(MongoObserver.create(
    url='mongodb://joaosaffran:saffran96@ds247648.mlab.com:47648/joaosaffran_tcc',
    db_name='joaosaffran_tcc'))

@ex.config
def config():
    episodes = 500
    log_dir = "./logs"
    max_features=1000
    hidden_dims=256
    embedding_dim=50
    max_length=20
    filters=256
    kernel_size=3
    gamma = 0.95
    epsilon = 1.0
    epsilon_min = 0.01
    epsilon_decay = 0.995
    learning_rate = 0.001
    code = '../../data/pi.c'

@ex.automain
@LogFileWriter(ex)
def main(_log, _run, code, episodes, max_features, hidden_dims,
        embedding_dim, max_length, filters,kernel_size, gamma,
        epsilon, epsilon_min, epsilon_decay, learning_rate,
        log_dir):

    _log.info("Starting ENV...")
    env = Code(code)
    _log.info("Config Agent")
    state_size = env.getInput().shape[0]
    action_size = np.shape(env.actions)[0]
    agent = QNet(state_size, action_size, max_features,
            hidden_dims, embedding_dim, max_length, filters,
            kernel_size, gamma, epsilon, epsilon_min,
            epsilon_decay, learning_rate)

    # agent.load("./save/cartpole-dqn.h5")
    done = False
    batch_size = 32
    _log.info("Starting Experiment")
    tf.summary.FileWriter(log_dir, graph=tf.get_default_graph())

    for e in range(episodes):
        state = env.reset()
        state = np.reshape(state, [1, state_size])
        r_sum = 0.0
        step_speedups = []
        for time in range(50):
            #env.render()
            action = agent.act(state)
            next_state, reward, done = env.step(action)
            reward = reward if not done else -10
            step_speedups.append(reward)
            next_state = np.reshape(next_state, [1, state_size])
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            r_sum += reward

            if done:
                break

        if len(agent.memory) > batch_size:
            agent.replay(batch_size)

        _run.log_scalar("training.reward", r_sum, e)
        _run.log_scalar("training.ep_max_reward", max(step_speedups), e)
        _run.log_scalar("training.global_max_speedup", env.max_speed_up, e)
        _run.log_scalar("training.epsilon", agent.epsilon, e)
        #_run.log_scalar("best_pragma", env.best_pragma, e)
        #agent.writer.flush()

        _log.info("episode: {}/{}, score: {}, e: {:.2} max speedup: {:.4}"
            .format(e, episodes, r_sum, agent.epsilon, env.max_speed_up))

        if e % 10 == 0:
            agent.save("./save/cartpole-dqn.h5")

    return env.best_pragma, env.max_speed_up
