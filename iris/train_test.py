# -*- coding: utf-8 -*-
from data_set import DataSet
from keras.models import load_model

__author__ = "ujihirokazuya"
__date__ = "2017/10/28"


def train():
    class_size_limit = 100  # int, can be 1-101 or None
    seq_length = 40
    image_shape = (80, 80, 1)

    data_set = DataSet(seq_length=seq_length, class_size_limit=class_size_limit, image_shape=image_shape)
    train_data_file_list, test_data_file_list = data_set.split_train_test()
    X, y = data_set.get_all_sequences_in_memory(train_data_file_list)
    X_test, y_test = data_set.get_all_sequences_in_memory(test_data_file_list)

    # Get the model.
    model = load_model("result_tmp.h5")
    loss_and_metrics = model.evaluate(X_test, y_test)
    print("\nloss:{} accuracy:{}".format(loss_and_metrics[0],loss_and_metrics[1]))


def main():
    train()


if __name__ == '__main__':
    main()
