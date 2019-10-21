#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tensorflow as tf
import numpy as np

sess = tf.Session()

# addition
print(sess.run(tf.add([1,2,3], [5,4,3])))

# subtraction
print(sess.run(tf.subtract([1,2,3], [5,4,3])))

# multiply
print(sess.run(tf.multiply([1,2,3], [5,4,3])))

# division
print(sess.run(tf.truediv([1,2,3], [5,4,3])))
# Note: div() will not give correct answer