import keras
from keras.datasets import mnist
from keras import backend as K
import numpy as np

from CutFivesec import CutFivesec

def NormalDataRead():
    num_classes = 10
    img_rows, img_cols = 28, 28

    #mnistをロード
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    #kerasの環境によってchannel_firstかlastか違うらしく、
    #それに応じてreshapeをする。
    #\.keras\keras.jsonによると自分はchannel_lastらしい
    if K.image_data_format() == 'channels_first':
        x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
        x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
        input_shape = (1, img_rows, img_cols)
    else:
        x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
        x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
        input_shape = (img_rows, img_cols, 1)

    #正規化とかの処理
    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    x_train /= 255
    x_test /= 255
    print('x_train shape:', x_train.shape)
    print(x_train.shape[0], 'train samples')
    print(x_test.shape[0], 'test samples')

    #one_hotに変換
    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)

    return input_shape, x_train, y_train, x_test, y_test


def PairDataRead():
    num_classes = 2
    img_rows, img_cols, frame = 200, 200, 150

    #mnistをロード
    wide_train = np.load("./video/test1.npy")

    #kerasの環境によってchannel_firstかlastか違うらしく、
    #それに応じてtransposeをする。
    #\.keras\keras.jsonによるとchannel_lastらしい
    if K.image_data_format() == 'channels_first':
        input_shape = (frame, img_rows, img_cols)
    else:
        wide_train = wide_train.transpose(0, 2, 3, 1)
        verch_train = verch_train.transpose(0, 2, 3, 1)
        input_shape = (img_rows, img_cols, frame)

    #正規化とかの処理
    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    x_train /= 255
    x_test /= 255
    print('x_train shape:', x_train.shape)
    print(x_train.shape[0], 'train samples')
    print(x_test.shape[0], 'test samples')

    #one_hotに変換
    # (yはuint8型)
    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)

    return input_shape, x_train, y_train, x_test, y_test
