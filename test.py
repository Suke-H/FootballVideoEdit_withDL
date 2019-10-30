import cv2

size = (200,200)
cap = cv2.VideoCapture("D:/VE/TRANS_DATA/1Q/wide/1.mp4")
#1フレーム分読み込み
for i in range(400):
    ret, frame = cap.read()
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
Img = cv2.resize(gray, size)

cv2.imwrite("D:/VE/TRANS_DATA/1Q/test2.jpg", Img)