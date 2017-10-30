# -*- coding: utf-8 -*-
import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 80)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 80)
fps = cap.get(cv2.CAP_PROP_FPS)
size = cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(fps)
print(size)


frames = list()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',gray)

    frame = cv2.resize(gray, (10, 10))
    # frame = cv2.resize(gray, (80, 80))
    frames.append(frame)
    if len(frames) == 40:
        frame_arr = np.array(frames)
        frame_arr = frame_arr[:, :, :, np.newaxis]
        print(frame_arr.shape)
        frames.clear()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
