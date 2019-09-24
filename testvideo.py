import numpy as np
import cv2

cap = cv2.VideoCapture("video/QT/1.mp4")
frame = cap.get(cv2.CAP_PROP_FRAME_COUNT)
fps = cap.get(cv2.CAP_PROP_FPS)
print(frame, frame/fps)
count = 0

while True:
    ret, frame = cap.read()

    if ret:
        count = count + 1
        #print(count)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.imshow('frame',gray)
        #if cv2.waitKey(1) & 0xFF == ord('q'):
            #break
        cv2.waitKey(1)

    else:
        break

cap.release()
cv2.destroyAllWindows()
print(count)