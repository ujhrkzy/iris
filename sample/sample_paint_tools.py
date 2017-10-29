# -*- coding: utf-8 -*-
import cv2
import numpy as np

# sx, syは線の始まりの位置
sx, sy = 0, 0
# ペンの色
color = (0, 0, 0)
# ペンの太さ
thickness = 1


# マウスの操作があるとき呼ばれる関数
def callback(event, x, y, flags, param):
    global img, sx, sy, color, thickness
    # マウスの左ボタンがクリックされたとき
    if event == cv2.EVENT_LBUTTONDOWN:
        sx, sy = x, y
    # マウスの左ボタンがクリックされていて、マウスが動いたとき
    if flags == cv2.EVENT_FLAG_LBUTTON and event == cv2.EVENT_MOUSEMOVE:
        cv2.line(img, (sx, sy), (x, y), color, thickness)
        sx, sy = x, y


# トラックバーを変更したらペンを変更
def changePencil(pos):
    global color, thickness
    r = cv2.getTrackbarPos("R", "img")
    g = cv2.getTrackbarPos("G", "img")
    b = cv2.getTrackbarPos("B", "img")
    color = (b, g, r)
    thickness = cv2.getTrackbarPos("T", "img")


# 画像を読み込む
img = cv2.imread("almond-0010.jpg")

# ウィンドウの名前を設定
image_view_name = "image_view_name"
cv2.namedWindow(image_view_name, cv2.WINDOW_NORMAL)

sample_view_name = "sample_view_name"
cv2.namedWindow(sample_view_name, cv2.WINDOW_NORMAL)
view_size = 500, 1000, 3
# view_size = 50, 50, 1
tmp_img = np.zeros(view_size, dtype=np.uint8)
text = "hello world"
# フォントの指定
# font = cv2.FONT_HERSHEY_COMPLEX_SMALL
# font = cv2.FONT_HERSHEY_SIMPLEX
font = cv2.FONT_HERSHEY_PLAIN
# 文字の書き込み
cv2.putText(tmp_img, text, (100, 100), font, 5, (255, 255, 0))
# def putText(img, text, org, fontFace, fontScale, color, thickness=None, lineType=None, bottomLeftOrigin=None): #
# real signature unknown; restored from __doc__
cv2.imshow(sample_view_name, tmp_img)

# マウス操作のコールバック関数の設定
cv2.setMouseCallback(image_view_name, callback)

# トラックバーのコールバック関数の設定
cv2.createTrackbar("R", image_view_name, 0, 255, changePencil)
cv2.createTrackbar("G", image_view_name, 0, 255, changePencil)
cv2.createTrackbar("B", image_view_name, 0, 255, changePencil)
cv2.createTrackbar("T", image_view_name, 1, 100, changePencil)

while (1):
    cv2.imshow(image_view_name, img)
    k = cv2.waitKey(1)

    # Escキーを押すと終了
    if k == 27:
        break
    # sを押すと画像を保存
    if k == ord("s"):
        cv2.imwrite("painted.png", img)
        break
