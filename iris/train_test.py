# -*- coding: utf-8 -*-
from data_set import DataSet
import numpy as np
from keras.models import load_model
import configuration

__author__ = "ujihirokazuya"
__date__ = "2017/10/28"

import tensorflow as tf

__author__ = "ujihirokazuya"
__date__ = "2017/11/03"


def train():
    class_size_limit = configuration.class_size_limit
    seq_length = configuration.seq_length
    image_shape = configuration.image_shape_and_color

    data_set = DataSet(seq_length=seq_length, class_size_limit=class_size_limit, image_shape=image_shape)
    train_data_file_list, test_data_file_list = data_set.split_train_test()
    # x, y = data_set.get_all_sequences_in_memory(train_data_file_list)
    x_test, y_test = data_set.get_all_sequences_in_memory(test_data_file_list)

    # Get the model.
    model = load_model(configuration.model_file_name)
    # loss_and_metrics = model.evaluate(X_test, y_test)
    # print("\nloss:{} accuracy:{}".format(loss_and_metrics[0],loss_and_metrics[1]))
    # x_test = x_test[0]
    x_test = x_test[5]
    print(x_test.shape)
    x_test = x_test[np.newaxis, :, :, :, :]
    print(x_test.shape)
    result = model.predict_classes(x_test, batch_size=1)
    print(result)
    result2 = model.predict(x_test, batch_size=1)
    print(result2)
    result3 = model.predict_proba(x_test, batch_size=1)
    print(result3)
    print(result3)


def main():
    train()


if __name__ == '__main__':
    main()
