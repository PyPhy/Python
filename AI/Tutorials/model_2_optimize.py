#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tensorflow as tf

# Model parameters
w = tf.Variable([0.3], tf.float32)
b = tf.Variable([-0.3], tf.float32)

# Inputs and Outputs
x = tf.placeholder(tf.float32)  # Inputs
linear_model = w* x + b         # model
y = tf.placeholder(tf.float32)  # known output

# Loss
squared_delta = tf.square(linear_model - y)
loss = tf.reduce_sum(squared_delta)

# Optimize
optimizer = tf.train.GradientDescentOptimizer(0.01)
train = optimizer.minimize(loss)

init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

for i in range(0, 1000 + 1):
    sess.run(train, { x: [1.0, 2.0, 3.0, 4.0],
                      y: [0.0, -1.0, -2.0, -3.0]})

print('New value of w is : ' + str(sess.run(w)))
print('New value of b is : ' + str(sess.run(b)))
