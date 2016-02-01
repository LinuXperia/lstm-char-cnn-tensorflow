import os
import numpy as np
import tensorflow as tf

from models import LSTMTDNN
from utils import *

from utils import pp

flags = tf.app.flags
flags.DEFINE_integer("epoch", 25, "Epoch to train [25]")
flags.DEFINE_integer("max_word_length", 65, "The maximum length of word [65]")
flags.DEFINE_integer("batch_size", 32, "The size of batch images [32]")
flags.DEFINE_float("learning_rate", 5e-5, "Learning rate [0.00005]")
flags.DEFINE_float("momentum", 0.9, "Momentum of RMSProp [0.9]")
flags.DEFINE_float("decay", 0.95, "Decay of RMSProp [0.95]")
flags.DEFINE_string("model", "LSTMTDNN", "The type of model to train and test [LSTM, LSTMTDNN]")
flags.DEFINE_string("data_dir", "data", "The name of data directory [data]")
flags.DEFINE_string("dataset", "ptb", "The name of dataset [ptb]")
flags.DEFINE_string("checkpoint_dir", "checkpoint", "Directory name to save the checkpoints [checkpoint]")
flags.DEFINE_boolean("forward_only", False, "True for forward only, False for training [False]")
FLAGS = flags.FLAGS

model_dict = {
  'LSTM': None,
  'LSTMTDNN': LSTMTDNN,
}

def main(_):
  pp.pprint(flags.FLAGS.__flags)

  if not os.path.exists(FLAGS.checkpoint_dir):
    print(" [*] Creating checkpoint directory...")
    os.makedirs(FLAGS.checkpoint_dir)

  with tf.Session() as sess:
    model = model_dict[FLAGS.model](checkpoint_dir=FLAGS.checkpoint_dir,
                                    forward_only=FLAGS.forward_only)

    if not FLAGS.forward_only:
      model.train(sess, FLAGS.dataset, FLAGS.max_word_length,
                  FLAGS.epoch, FLAGS.batch_size, FLAGS.learning_rate,
                  FLAGS.decay, FLAGS.data_dir)
    else:
      model.load(FLAGS.checkpoint_dir)

if __name__ == '__main__':
  tf.app.run()
