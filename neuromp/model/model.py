from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Embedding
from keras.layers import Conv1D, GlobalMaxPooling1D
from keras.optimizers import Adam
import numpy as np
import random

from neuromp.preprocessing.code import Code

EPISODES = 1000

class QNet(object):
    def __init__(self, state_size, actions_size, max_features=5000, hidden_dims=256,
                  embedding_dim=50, max_length=20, filters=256, kernel_size=3):

        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=100)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001

        self.model = Sequential()
        self.model.add(Embedding(max_features,
                                embedding_dim,
                                input_length=max_length
        ))
        self.model.add(Conv1D(filters,
                              kernel_size,
                              padding='valid',
                              activation='relu',
                              strides=1
        ))
        self.model.add(GlobalMaxPooling1D())

        self.model.add(Dense(hidden_dims, activation='relu'))
        self.model.add(Dense(actions_size, activation='softmax'))

        self.model.compile(loss='mse',
            optimizer=Adam(lr=self.learning_rate))

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])  # returns action

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma *
                            np.amax(self.model.predict(next_state)[0]))
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


if __name__ == "__main__":
    env = Code('../data/pi.c')
    state_size = env.getInput().shape[0]
    action_size = np.shape(env.actions)[0]
    agent = QNet(state_size, action_size)
    # agent.load("./save/cartpole-dqn.h5")
    done = False
    batch_size = 32

    for e in range(EPISODES):
        state = env.reset()
        state = np.reshape(state, [1, state_size])
        r_sum = 0.0
        for time in range(50):
            #env.render()
            action = agent.act(state)
            next_state, reward, done = env.step(action)
            reward = reward if not done else -10
            next_state = np.reshape(next_state, [1, state_size])
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            r_sum += reward

            if done:
                break

        print("episode: {}/{}, score: {}, e: {:.2} max speedup: {:.4}"
            .format(e, EPISODES, r_sum, agent.epsilon, env.max_speed_up))

        if len(agent.memory) > batch_size:
            agent.replay(batch_size)
        # if e % 10 == 0:
        #     agent.save("./save/cartpole-dqn.h5")
