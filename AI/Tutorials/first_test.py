#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tensorflow as tf

# Model parameters
a = tf.Variable([10.0], tf.float32)
b = tf.Variable([1.0], tf.float32)

# Inputs and Outputs
x = tf.placeholder(tf.float32)            # Inputs
Square_model = a* x + b                   # model
y = tf.placeholder(tf.float32)            # known output

# Loss
squared_delta = tf.square(Square_model - y)
loss = tf.reduce_sum(squared_delta)

# Optimize
optimizer = tf.train.GradientDescentOptimizer(0.01)
train = optimizer.minimize(loss)

# Start the session
init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

for i in range(0, 1000 + 1):  # 1000 epoch
    sess.run(train, { x: [1.0, 2.0, 3.0, 4.0],
                      y: [2.0, 4.0, 6.0, 8.0]})
    
print('New value of a is : ' + str(sess.run(a)))
print('New value of b is : ' + str(sess.run(b)))
