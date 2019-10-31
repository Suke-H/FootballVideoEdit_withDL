import os
from glob import glob
import subprocess
import re
import time


###データをMTS形式からmp4形式に変換する工程###
#source_dir_path: データが入っているディレクトリのパス
#trans_dir_path:　データを移す場所

def VideoTrans(source_dir_path, trans_dir_path):

    start = time.time()

    # source/長県戦/1Q,  source/長県戦/2Qのようなパスを取得
    folders = glob(source_dir_path + "/**/**")

    for folder in folders:
        # 各フォルダ内の全ての動画のパスを読み込んで、ソート
        # reの[]内は例えば"10.MTS"の"10"を抽出したいのでlen-1にしている
        paths = sorted(glob(folder + "/**.MTS"),
                           key=lambda s: int(re.findall(r'\d+', s)[len(re.findall(r'\d+', s)) - 1]))

        # folderから"長県戦/1Q"の部分を抽出
        Q = os.path.basename(folder)
        dir = os.path.dirname(folder)
        match = os.path.basename(dir)

        #print(match + "/" + Q, len(paths))

        for path in paths:
            # "長県戦/1Q/10.MTS"のようなパスを作成
            root, _ = os.path.splitext(path)
            filename = os.path.basename(root) + ".mp4"
            file_path = match + "/" + Q + "/" + filename

            #print(file_path)

            ###ターミナル上でffmpegに「MTS->mp4」を命令###

            #正常に変換されるが、かなり時間かかる
            #cmd = "ffmpeg -i " + path + " " + trans_dir_path + "/" + file_path

            #早く終わるがよくわからんくなる(おそらく解決)
            cmd = "ffmpeg -i " + path + " -vcodec copy -acodec copy " + trans_dir_path + "/" + file_path

            subprocess.call(cmd, shell=True)

    end = time.time()
    print("time:{}m".format((end-start)/60))


VideoTrans("D:/2018data", "D:/2018mp4")




