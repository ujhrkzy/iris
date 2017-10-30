# -*- coding: utf-8 -*-
import cv2
import numpy as np
from keras.models import load_model
import csv

import configuration

__author__ = "ujihirokazuya"
__date__ = "2017/10/28"


class Demo(object):

    # _seq_size = 40
    _seq_size = 150
    # _count_size = 3
    _count_size = 1
    _image_shape = (80, 80)

    def __init__(self):
        self.category_dict = dict()
        with open("data/data_list/class_id.txt", "r") as f:
            reader = csv.reader(f, delimiter=" ")
            for row in reader:
                self.category_dict[int(row[0])] = row[1]
        model = load_model(configuration.model_file_name)
        self.model = model
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FPS, 30)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 80)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 80)
        fps = cap.get(cv2.CAP_PROP_FPS)
        size = cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print("fps:{}".format(fps))
        print("video size:{}".format(size))
        self.video_capture = cap

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.video_capture.release()
        cv2.destroyAllWindows()

    def _predict(self, frames):
        frames = np.array(frames)
        frames = frames[:, :, :, np.newaxis]
        frames = (frames / 255.).astype(np.float32)
        x_test = frames[np.newaxis, :, :, :, :]
        result = self.model.predict_classes(x_test, batch_size=1)
        print(result)
        print(self.category_dict.get(result[0]))
        # result2 = self.model.predict(x_test, batch_size=1)
        # print(result2)

    def execute(self):
        frames = list()
        count = 0
        print("fps:{}".format(self.video_capture.get(cv2.CAP_PROP_FPS)))
        print("w:{}".format(self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)))
        print("h:{}".format(self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        is_valid = False
        while True:
            _, frame = self.video_capture.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if cv2.waitKey(1) & 0xFF == ord('e'):
                is_valid = not is_valid
            if is_valid:
                if self._can_add_frame(count):
                    self._add_frames(frames, gray)
                count += 1
                if self._can_predict(frames):
                    self._predict(frames)
                    frames.clear()
                    is_valid = False
                    count = 0
                print(count)
            if is_valid:
                text = "valid"
            else:
                text = "invalid"
            font = cv2.FONT_HERSHEY_PLAIN
            cv2.putText(gray, text, (10, 30), font, 2, (0, 0, 0))
            cv2.imshow('frame', gray)

    def _add_frames(self, frames: list, gray):
        frame = cv2.resize(gray, self._image_shape)
        frames.append(frame)
        print(len(frames))

    def _can_add_frame(self, count: int):
        return count % self._count_size == 0

    def _can_predict(self, frames: list):
        return len(frames) == self._seq_size


def main():
    demo = Demo()
    with demo:
        demo.execute()


if __name__ == '__main__':
    main()
