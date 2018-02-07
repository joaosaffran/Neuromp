import tensorflow as tf
import numpy as np
from collections import deque


class Memory(object):
    def __init__(self, max_size = 1000):
        self.buffer = deque(maxlen=max_size)

    def add(self, experience):
        self.buffer.append(experience)

    def sample(self, batch_size):
        idx = np.random.choice(np.arange(len(self.buffer)),
                               size=batch_size,
                               replace=False)
        return [self.buffer[ii] for ii in idx]


class QNet(object):

    def __init__(self, action_size, state_size, hidden_size=128, lr=0.01):

        self.inputs = tf.placeholder(tf.float32, [None, state_size], name="inputs")

        self.actions = tf.placeholder(tf.int32, [None], name="actions")
        self.one_hot_actions = tf.one_hot(self.actions, action_size)

        self.targetQs = tf.placeholder(tf.float32, [None], "target")

        self.l1 = tf.contrib.fully_connected(self.inputs, hidden_size)
        self.l2 = tf.contrib.fully_connected(self.l1, hidden_size)

        self.output = tf.contrib.fully_connected(self.l2, action_size, activation_fn=None)

        self.Q = tf.reduce_sum(tf.multiply(self.output, self.one_hot_action), axis=1)
        self.loss = tf.reduce_mean(tf.square(self.targetQs - self.Q))
        self.optimizer = tf.train.AdamOptimizer(lr).minimize(self.loss)

    def fit(self, initial_state):
        pass
