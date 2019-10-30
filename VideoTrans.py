import cv2
import os
import numpy as np
from glob import glob
import subprocess
import re
import shutil
import random

###データをMTS形式からmp4形式に変換する工程###
#source_dir_path: データが入っているディレクトリのパス
#trans_dir_data:　データを移す場所

def VideoTrans(source_dir_path, trans_dir_data):

    #ソースディレクトリ内の全ての動画のパスを読み込んで、ソート
    ori_paths = sorted(glob(source_dir_path + "/**.MTS"), key=lambda s: int(re.findall(r'\d+', s)[1]))
    print(ori_paths)

    for i, path in enumerate(ori_paths):

        #wideは0.mp4, 1.mp4のように命名
        if i % 2 == 0:
            file_name = str(i//2) + '.mp4'
        #verchは0v.mp4, 1v.mp4のように命名
        else:
            file_name = str(i//2) + 'v.mp4'

        ###ターミナル上でffmpegに「MTS->mp4」を命令###

        #正常に変換されるが、かなり時間かかる
        #cmd = "ffmpeg -i " + path + " " + trans_dir_data + "/" + file_name

        #早く終わるがよくわからんくなる(おそらく解決)
        cmd = "ffmpeg -i " + path + " -vcodec copy -acodec copy " + trans_dir_data + "/" + file_name

        subprocess.call(cmd, shell=True)

VideoTrans("D:/VE/長県戦/1Q", "D:/VE/長県戦/1Qtrans")




