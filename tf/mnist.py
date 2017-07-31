# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""A very simple MNIST classifier.

See extensive documentation at
https://www.tensorflow.org/get_started/mnist/beginners
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import sys

from tensorflow.examples.tutorials.mnist import input_data

import tensorflow as tf

FLAGS = None

BATCH_SIZE = 128
N_ITERATIONS = 500
N_EPCOCHS = 4


def main(_):
    # Import data
    mnist = input_data.read_data_sets(FLAGS.data_dir, one_hot=True)

    # Create the model
    x = tf.placeholder(tf.float32, [None, 784])
    x2 = tf.reshape(x, [-1, 28, 28, 1])
    net = tf.layers.conv2d(x2, 20, [5, 5], activation=tf.nn.relu)
    net = tf.layers.max_pooling2d(net, [2, 2], [2, 2])
    net = tf.layers.conv2d(net, 50, [5, 5], activation=tf.nn.relu)
    net = tf.layers.max_pooling2d(net, [2, 2], [2, 2])
    net = tf.contrib.layers.flatten(net)
    net = tf.layers.dense(net, 500, activation=tf.nn.relu)
    y = tf.layers.dense(net, 10, activation=tf.nn.softmax)

    # Define loss and optimizer
    y_ = tf.placeholder(tf.float32, [None, 10])

    cross_entropy = tf.reduce_mean(
        tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
    train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

    sess = tf.InteractiveSession()
    tf.global_variables_initializer().run()
    # Train
    for epochid in range(N_EPCOCHS):
        print("Running epoch %d ..." % epochid)
        for iterid in range(N_ITERATIONS):
            sys.stdout.write('\r %d/%d' % (iterid+1, N_ITERATIONS))
            batch_xs, batch_ys = mnist.train.next_batch(batch_size=BATCH_SIZE)
            sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

        # Test trained model
        correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        print(" --> Accuracy: ", sess.run(accuracy, feed_dict={x: mnist.test.images,
                                            y_: mnist.test.labels}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default='/tmp/tensorflow/mnist/input_data',
                        help='Directory for storing input data')
    FLAGS, unparsed = parser.parse_known_args()
    tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)