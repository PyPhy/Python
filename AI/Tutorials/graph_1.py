#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tensorflow as tf
import numpy as np

sess = tf.Session()

x_vals = np.array([1.0, 3.0, 5.0, 7.0, 9.0])
x_data = tf.placeholder(tf.float32)
m_const = tf.constant(3.0)
my_product = tf.multiply(x_data, m_const)

for x_val in x_vals:
    Look = sess.run(my_product, feed_dict = {x_data: x_val})
    print(Look)
