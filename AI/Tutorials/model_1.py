#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tensorflow as tf

# Model parameters
w = tf.Variable([-1.0], tf.float32)
b = tf.Variable([1.0], tf.float32)

# Inputs and Outputs
x = tf.placeholder(tf.float32)

linear_model = w* x + b

y = tf.placeholder(tf.float32)

# Loss
squared_delta = tf.square(linear_model - y)
loss = tf.reduce_sum(squared_delta)

init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)


print(sess.run(loss, { x: [1, 2, 3, 4],
                       y: [0, -1, -2, -3]}))

# The code goes like this

# sess.run(loss, ...) will give the values of x and y , [1, 2, 3, 4] and [0, -1, -2, -3] respectively.
# w = 0.3 , b = -0.3
# Now, linear_model = w* x + b
#                   = 0.3* [1, 2, 3, 4] -0.3 = [0, 0.3, 0.6, 0.9]
# squared_delta = (linear_model - y)**2
#               = ([0, 0.3, 0.6, 0.9] - [0, -1, -2, -3])**2 = [0, 1.69, 6.76, 15.21]

# loss = sum(squared_delta)
#      = sum( [0, 1.69, 6.76, 15.21]) = 23.66

# So, answer is 23.66
