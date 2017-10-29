# -*- coding: utf-8 -*-
from keras.preprocessing.image import img_to_array, load_img
import numpy as np

__author__ = "ujihirokazuya"
__date__ = "2017/10/28"


def process_image(image_file_path, target_shape, gray_scale=False):
    h, w, _ = target_shape
    image = load_img(image_file_path, target_size=(h, w), grayscale=gray_scale)
    img_arr = img_to_array(image)
    x = (img_arr / 255.).astype(np.float32)
    return x
