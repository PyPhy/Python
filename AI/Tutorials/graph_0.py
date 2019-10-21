#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tensorflow as tf

sess = tf.Session()

placeholder_ex_one = tf.placeholder(tf.float32)
placeholder_ex_two = tf.placeholder(tf.float32)
placeholder_ex_tre = tf.placeholder(tf.float32)

placeholder_summation = tf.add_n([placeholder_ex_one, placeholder_ex_two, placeholder_ex_tre])

File_Writer = tf.summary.FileWriter('/home/divyang/Documents/Python/AI/Tensorflow_tutorials/graph', sess.graph)

Look = sess.run(placeholder_summation, feed_dict = {placeholder_ex_one: 10,
                                                    placeholder_ex_two: 20,
                                                    placeholder_ex_tre: 30} )

# tensorboard --logdir="TensorFlow"
sess.close()