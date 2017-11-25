# -*- coding: utf-8 -*-

__author__ = "ujihirokazuya"
__date__ = "2017/10/28"

model = "conv3d"
class_size_limit = 100  # int, can be 1-101 or None
seq_length = 40
# frame_skip_size = 3
frame_skip_size = 1
# seq_length = 150
image_shape_and_color = (80, 80, 1)
image_shape = (80, 80)
# image_shape = (80, 80, 3)

# model_file_name = "result_tmp.h5"
model_file_name = "result_tmp_seq_len_40.h5"
# model_file_name = "result_tmp_seq_len_150.h5"
