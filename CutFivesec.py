import cv2
#import sys
import numpy as np
from glob import glob
import re

##################################################################
#  作成した動画データセットを読み込む際に、動画をグレースケールかつ200*200にリサイズして
#  動画の最後から150フレームとることにより、
#　[N, 150, 200, 200]となるデータセットを作成し、npy形式で保存する
#################################################################
# (おそらく5秒 = 150フレーム)
# dir_path: 動画データセットの場所
def CutFivesec(source_dir_path, trans_dir_data, filename):

    #ソースディレクトリ内の全ての動画のパスを読み込んで、ソート
    paths = sorted(glob(source_dir_path + "/**"), key=lambda s: int(re.findall(r'\d+', s)[len(re.findall(r'\d+', s))-1]))

    videos = []

    for path in paths:
        #ビデオ読み込み
        cap = cv2.VideoCapture(path)
        #frame = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        #fps = cap.get(cv2.CAP_PROP_FPS)

        #いる？
        #if not cap.isOpened():
            #sys.exit()
  
        one_video = []
        print(path)
        #print("frame:{}, fps:{}, time:{}s".format(frame, fps, frame / fps))
        real_frame = 0

        while True:
            #1フレーム分読み込み
            ret, frame = cap.read()

            if ret:
                #グレースケールに変換
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                #200*200にリサイズ
                gray = cv2.resize(gray, (200,200))
                #one_videoに1フレームずつappend
                one_video.append(gray)

                real_frame = real_frame + 1

            else:
                break

        #print(np.asarray(one_video[int(-1*fps*10//1):]).shape, real_frame)

        #動画の最後から150フレーム取ってappend
        videos.append(one_video[-150:])

    videos = np.array(videos)
    print(videos.shape)

    #[N, 150, 200, 200]の動画データセットを一つのnpyファイルにして保存
    np.save(trans_dir_data + "/" + filename, videos)


CutFivesec("D:/VE/TRANS_DATA/1Q/wide", "D:/VE/TRANS_DATA/1Q", "test1")