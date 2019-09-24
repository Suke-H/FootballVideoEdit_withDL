import cv2
import sys
import numpy as np
from glob import glob
import re


paths = sorted(glob("video/QTT/**"), key=lambda s: int(re.search(r'\d+', s).group()))

videos = []

for path in paths:
    #ビデオ読み込み
    cap = cv2.VideoCapture(path)
    frame = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = cap.get(cv2.CAP_PROP_FPS)

    #いる？
    #if not cap.isOpened():
        #sys.exit()
  
    one_video = []
    print(path)
    print("frame:{}, fps:{}, time:{}s".format(frame, fps, frame / fps))
    real_frame = 0

    while True:
        #1フレーム分読み込み
        ret, frame = cap.read()

        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            one_video.append(gray)

            real_frame = real_frame + 1

        else:
            break

    print(np.asarray(one_video)[int(-1*fps*10//1):].shape, real_frame)


