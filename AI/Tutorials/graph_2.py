#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tensorflow as tf
import numpy as np

sess = tf.Session()

my_array = np.array([ [1.0, 3.0, 5.0, 7.0, 9.0],
                      [-2.0, 0.0, 2.0, 4.0, 6.0],
                      [-6.0, -3.0, 0.0, 3.0, 6.0] ])

x_vals = np.array([my_array, my_array + 1])
x_data = tf.placeholder(tf.float32, shape = (3,5) )

#%%
m1 = tf.constant([ [1.0], [0.0], [-1.0], [2.0], [4.0] ])
m2 = tf.constant([ [2.0] ])
a1 = tf.constant([ [10.0] ])

Look_m1 = sess.run(m1)
Look_m2 = sess.run(m2)
Look_a1 = sess.run(a1)

#%%
prod1 = tf.matmul(x_data, m1)
prod2 = tf.matmul(prod1, m2)
add1 = tf.add(prod2, a1)

for x_val in x_vals:
    Look = sess.run(add1, feed_dict = {x_data: x_val} )
    print(Look)
    
#%% Explaination :
# x_val will first take value of first matrix from x_vals which has (3,5) dimension
# then it will start doing oparations from prod1, prod2 to add1
# After compliting first loop, x_val will take second value and do the same process    
