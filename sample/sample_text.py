import cv2
import numpy as np


# スケールの書き込み関数
def make_scale(im, length=40, from_edge=15, thick=2, hight=6, font_size=0.6, pix_size=10):
    w = im.shape[0]
    h = im.shape[1]
    # 横線
    cv2.line(im, (w - length - from_edge, h - from_edge), (w - from_edge, h - from_edge), (255, 255, 0), thick)
    # 縦線左
    cv2.line(im, (10, 10), (10, 30), (255, 0, 0), thick)
    # 縦線右
    cv2.line(im, (10, 20), (30, 50), (255, 0, 0), thick)

    # 1ピクセルのサイズから長さを計算
    size = pix_size * length
    text = str(size) + 'micro m'
    # フォントの指定
    # font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    # font = cv2.FONT_HERSHEY_SIMPLEX
    font = cv2.FONT_HERSHEY_PLAIN
    # 文字の書き込み
    cv2.putText(im, text, (w - length - from_edge - 5, h - from_edge - hight), font, font_size, (255, 255, 0))
    cv2.putText(im, text, (100, 100), font, font_size, (255, 255, 0))

    return im


if __name__ == '__main__':
    view_size = 1000, 1000, 3
    im = np.zeros(view_size, dtype=np.uint8)
    # im = cv2.imread("almond-0010.jpg")
    im2 = make_scale(im)
    cv2.imshow("", im2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
