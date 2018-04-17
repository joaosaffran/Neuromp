from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Embedding
from keras.layers import Conv1D, GlobalMaxPooling1D
from keras.optimizers import Adam
import tensorflow as tf
import numpy as np
import random


class QNet(object):
    def __init__(self, state_size, actions_size, max_features=5000, hidden_dims=256,
                  embedding_dim=50, max_length=20, filters=256, kernel_size=3,
                  gamma=0.95, epsilon=1.0, epsilon_min=0.01, epsilon_decay=0.995, learning_rate=0.0001,
                  log_dir='./logs'):

        self.log_dir = log_dir
        self.state_size = state_size
        self.action_size = actions_size
        self.memory = deque(maxlen=100)
        self.gamma = gamma    # discount rate
        self.epsilon = epsilon  # exploration rate
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.learning_rate = learning_rate

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

        self.writer = tf.summary.FileWriter(self.log_dir, graph=tf.get_default_graph())

    def log_scalar(self, tag, value, step):
        summary = tf.Summary(value=[tf.Summary.Value(tag=tag,
                                                     simple_value=value)])
        self.writer.add_summary(summary, step)

    def log_string(self, tag, value, step):
        text_tensor = tf.make_tensor_proto(value, dtype=tf.string)
        meta = tf.SummaryMetadata()
        meta.plugin_data.plugin_name = "text"
        summary = tf.Summary()
        summary.value.add(tag=tag, metadata=meta, tensor=text_tensor)
        self.writer.add_summary(summary, step)

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
