#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tensorflow as tf
import numpy as np

row_dim = 3
col_dim = 3

sess = tf.Session()
#%% Fixed tensors

# Zero filled tensor
zero_tsr = tf.zeros([row_dim, col_dim])
Look_zero_tsr = sess.run(zero_tsr)
# output ---> <tf.Tensor 'zeros:0' shape=(3, 3) dtype=float32>

# Create a one filled tensor
ones_tsr = tf.ones([row_dim, col_dim])

# Constant filled tensor
filled_tsr = tf.fill([row_dim, col_dim], 42)
Look_filled_tsr = sess.run(filled_tsr)

# create a tensor out of existing constant
constant_tsr = tf.constant([1,2,3])
Look_constant_tsr = sess.run(constant_tsr)


#%% Sequence tensors

# linspace() like tensor
linear_tsr = np.linspace(0, 1, 3)
linear_tsr = tf.convert_to_tensor(linear_tsr)    # convert into tensor
Look_linear_tsr = sess.run(linear_tsr)

# 
integer_seq_tsr = tf.range(start = 6, limit = 15, delta = 3) # [6,9,12]
Look_interger_seq_tsr = sess.run(integer_seq_tsr)


#%% Random tensors

# random numbers from uniform distribution
randunif_tsr = tf.random_uniform([row_dim, col_dim], minval = 2, maxval = 6)  # minval <= x < maxval
Look_randunif_tsr = sess.run(randunif_tsr)

#%% Variable

my_var = tf.Variable(tf.zeros([row_dim, col_dim]))
