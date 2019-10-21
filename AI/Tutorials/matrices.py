#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tensorflow as tf
import numpy as np

sess = tf.Session()

#%% Creating matrices

I = tf.diag([1.0, 1.0, 1.0])
A = tf.truncated_normal([2,3])
B = tf.fill([2,3], 5.0)
C = tf.random_uniform([3,2])
D = tf.convert_to_tensor(np.array([ [1.0, 2.0, 3.0],
                                    [-3.0, -7.0, -1.0],
                                    [0.0, 5.0, -2.0] ]))

Look_I = sess.run(I)
Look_A = sess.run(A)
Look_B = sess.run(B)
Look_C = sess.run(C)
Look_D = sess.run(D)


#%% Operations

Add = sess.run(A+B)
Sub = sess.run(B-B)

# matrix multiplication
Mul = sess.run(tf.matmul(B, I))

# Transpose
Tra = sess.run(tf.transpose(C))

# Inverse
Inv = sess.run(tf.matrix_inverse(D))

# Cholesky decomposition
Cho = sess.run(tf.cholesky(I))

# Eigen value and Eigen vectors
Eig = sess.run(tf.self_adjoint_eig(D))
# Note: self_adjoint_eig() outputs eigen values in first row and the subvectors in the remaining vectors