"""
import cv2

size = (200,200)
cap = cv2.VideoCapture("D:/VE/TRANS_DATA/1Q/wide/1.mp4")
#1フレーム分読み込み
for i in range(400):
    ret, frame = cap.read()
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
Img = cv2.resize(gray, size)

cv2.imwrite("D:/VE/TRANS_DATA/1Q/test2.jpg", Img)
"""

"""
import numpy as np
import random

num = 10

#巡回置換する動画の番号リストをランダムで作成
change_list = sorted(random.sample([i for i in range(num)], num//2))

#先頭をpopして、それを末尾にappendすれば巡回置換
tmp = change_list.pop(0)
change_list.append(tmp)

print(change_list)
targets = []

for i in range(num):
    if i not in change_list:
        change_list.insert(i, i)
        targets.append(1)

    else:
        targets.append(0)

a = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
print(change_list)
print(a[change_list])
print(targets)
"""

import numpy as np

paths = np.array(["D:/VE/長県戦/1QT/0.mp4","D:/VE/長県戦/1QT/1.mp4"])

np.savetxt("test.txt", paths, fmt="%s")






