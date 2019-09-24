import cv2
import ffmpeg as fp
import os
import numpy as np
from glob import glob
import subprocess
import re
import shutil
import random


###ペアのデータを作成する工程###
#source_dir_path: データが入っているディレクトリのパス
#                 (データはすでに編集されて、wide/verchが混合してるもの)
#trans_dir_data :　データを移す場所
#  ├ /wide      :  wideのデータセット
#  ├ /verch     :  verchのデータセット
#  ├ targets.npy:  正解ラベル

def MakePairData(source_dir_path, trans_dir_path):
    #ソースディレクトリ内の全ての動画のパスを読み込んで、ソート
    trans_paths = sorted(glob(source_dir_path + "/**.mp4"), key=lambda s: int(re.findall(r'\d+', s)[1]))

    #新規フォルダ作成
    os.mkdir(trans_dir_path + "/wide")
    os.mkdir(trans_dir_path + "/verch")

    #wide(=verch)の動画数
    num = len(trans_paths)//2
    print(num)

    #wideのビデオは順序を変えずに移す
    for i in range(num):
        file_name = str(i) + ".mp4"
        shutil.copyfile(trans_paths[2*i], trans_dir_path + "/wide" + file_name)

    #verchの操作。。。
    #巡回置換する動画の番号リストをランダムで作成
    hange_list = sorted(random.sample([i for i in range(num)], num//2))
    print(change_list)

    """
    #巡回置換するため、[1,2,3,...,num-1,0]というリストを作成
    #cyclic_list = [i for i in range(1, len(change_list))]
    #cyclic_list.append(0)
    #print(cyclic_list)

    #change_listを巡回置換
    # ( a=[0,2,4]のとき、a[[1,2,0]] == [2,4,0] )
    #after_change_list = change_list[cyclic_list]
    #print(after_change_list)
    """

    #先頭をpopして、それを末尾にappendすれば巡回置換
    after_change_list = change_list[:]
    tmp = after_change_list.pop(0)
    after_change_list.append(tmp)
    print(after_change_list)

    targets = []

    for i in range(num):
        #change_listに載ってたやつは巡回置換して移す
        if i in change_list:
            idx = change_list.index(i)
            file_name = str(after_change_list[idx]) + "v.mp4"
            shutil.copyfile(trans_paths[2*i+1], trans_dir_path + "/verch" + file_name)
            #正解ラベルは0
            targets.append(0)

        #載ってなかったらそのままの順番で移す
        else:
            file_name = str(i) + "v.mp4"
            shutil.copyfile(trans_paths[2*i+1], trans_dir_path + "/verch" + file_name)
            #正解ラベルは1
            targets.append(1)

    #正解ラベルを保存
    np.array(targets, dtype="uint8")
    np.save(trans_dir_data + "/targets", targets)
    