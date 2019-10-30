import os
import numpy as np
from glob import glob
import re
import shutil
import random

from CutFivesec import CutFivesec

###ペアのデータを作成する工程###
#source_dir_path: データが入っているディレクトリのパス
#                 (データはすでに編集されて、wide/verchが混合してるもの)
#trans_dir_data :　データを移す場所
#  ├ /wide      :  wideのデータセット
#  ├ /verch     :  verchのデータセット
#  ├ /targets   :  正解ラベル

def MakePairData(source_dir_path, trans_dir_path):
    # ソースディレクトリ内の全ての動画のパスを読み込んで、ソート
    # reの[]内は例えば"10.mp4"の"10"を抽出したいのでlen-2にしている
    trans_paths = sorted(glob(source_dir_path + "/**.mp4"), key=lambda s: int(re.findall(r'\d+', s)[len(re.findall(r'\d+', s))-2]))
    print(trans_paths)

    #wide(=verch)の動画数
    num = len(trans_paths)//2
    print("video_num:{}*2".format(num))

    wide_paths = []
    verch_paths = []

    #全動画のパスをwide,verchに分ける
    for path in trans_paths:
        #wide
        if "v" not in os.path.basename(path):
            wide_paths.append(path)
        #verch
        else:
            verch_paths.append(path)

    # verchの操作
    # 巡回置換する動画の番号リストをランダムで作成
    change_list = sorted(random.sample([i for i in range(num)], num//2))

    # 先頭をpopして、それを末尾にappendすれば巡回置換
    tmp = change_list.pop(0)
    change_list.append(tmp)

    #正解ラベル
    targets = []

    #巡回置換しない番号を挿入
    for i in range(num):
        if i not in change_list:
            change_list.insert(i, i)
            targets.append(1)

        else:
            targets.append(0)

    print(change_list)
    print(targets)

    #verchのパスを並び替え(一応listに直した)
    verch_paths = list(np.array(verch_paths)[change_list])

    #名前は長県戦_1Qなどにする
    Q = os.path.basename(source_dir_path)
    dir = os.path.dirname(source_dir_path)
    match = os.path.basename(dir)
    filename = match + "_" + Q

    #150フレームに切ったものを保存
    CutFivesec(wide_paths, trans_dir_path + "/wide", filename)
    CutFivesec(verch_paths, trans_dir_path + "/verch", filename)

    #正解ラベルを保存
    np.array(targets, dtype="uint8")
    np.save(trans_dir_path + "/targets/" + filename, targets)

MakePairData("D:/VE/長県戦/1Qtrans", "D:/VE/TRANS_DATA")