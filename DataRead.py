import keras
from keras.datasets import mnist
from keras import backend as K
import numpy as np
from glob import glob
import re
import time
import random

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


def PairDataRead(dir_path):
    start = time.time()

    num_classes = 2
    img_rows, img_cols, frame = 200, 200, 30

    # 動画データセットをロード
    # reの[]内は例えば"西南_1Q.npy"の"1"を抽出したいのでlen-1にしている
    wide_paths = sorted(glob(dir_path + "/wide/**.npy"),\
                        key=lambda s: int(re.findall(r'\d+', s)[len(re.findall(r'\d+', s))-1]))
    wide_data = np.concatenate([np.load(wide_paths[i]) for i in range(len(wide_paths)-len(wide_paths)+4)], axis=0)
    verch_paths = sorted(glob(dir_path + "/verch/**.npy"), \
                         key=lambda s: int(re.findall(r'\d+', s)[len(re.findall(r'\d+', s)) - 1]))
    verch_data = np.concatenate([np.load(verch_paths[i]) for i in range(len(verch_paths)-len(verch_paths)+4)], axis=0)

    # 正解ラベルをロード
    targets_paths = sorted(glob(dir_path + "/targets/**.npy"), \
                           key=lambda s: int(re.findall(r'\d+', s)[len(re.findall(r'\d+', s)) - 1]))
    targets_data = np.concatenate([np.load(targets_paths[i]) for i in range(len(targets_paths)-len(targets_paths)+4)], axis=0)

    # 減らしてみる...
    wide_data = wide_data[:, 120:150, :, :]
    verch_data = verch_data[:, 120:150, :, :]

    # 訓練データと検証データに分ける(9:1にする)
    N = wide_data.shape[0]
    perm = np.random.permutation(N)
    N1 = int(N*0.9)

    wide_train = wide_data[perm[:N1]]
    wide_test = wide_data[perm[N1:N]]
    verch_train = verch_data[perm[:N1]]
    verch_test = verch_data[perm[N1:N]]
    y_train = targets_data[perm[:N1]]
    y_test = targets_data[perm[N1:N]]

    print("TRAIN...wide:{}, verch:{}, targets:{}".format(wide_train.shape, verch_train.shape, y_train.shape))
    print("TEST...wide:{}, verch:{}, targets:{}".format(wide_test.shape, verch_test.shape, y_test.shape))

    #kerasの環境によってchannel_firstかlastか違うらしく、
    #それに応じてtransposeをする。
    #\.keras\keras.jsonによるとchannel_lastらしい
    if K.image_data_format() == 'channels_first':
        input_shape = (frame, img_rows, img_cols)
    else:
        wide_train = wide_train.transpose(0, 2, 3, 1)
        wide_test = wide_test.transpose(0, 2, 3, 1)
        verch_train = verch_train.transpose(0, 2, 3, 1)
        verch_test = verch_test.transpose(0, 2, 3, 1)
        input_shape = (img_rows, img_cols, frame)

    #正規化とかの処理
    wide_train = wide_train.astype('float32')
    wide_test = wide_test.astype('float32')
    verch_train = verch_train.astype('float32')
    verch_test = verch_test.astype('float32')
    wide_train /= 255
    wide_test /= 255
    verch_train /= 255
    verch_test /= 255

    # 正解ラベル読み込み

    return input_shape, wide_train, verch_train, y_train, wide_test, verch_test, y_test

    end = time.time()
    print("time:{}m".format((end-start)/60))

def MNISTPairRead():
    img_rows, img_cols = 28, 28

    # mnistをロード
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    # verchの操作
    # 巡回置換する動画の番号リストをランダムで作成
    num = x_train.shape[0]
    change_list = sorted(random.sample([i for i in range(num)], num // 2))

    # 先頭をpopして、それを末尾にappendすれば巡回置換
    tmp = change_list.pop(0)
    change_list.append(tmp)

    # 正解ラベル
    targets = []


#PairDataRead("D:/VE/TRANS_DATA")