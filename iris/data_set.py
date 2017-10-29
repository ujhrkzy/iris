# -*- coding: utf-8 -*-
import csv
import numpy as np
import random
import glob
import operator
from processor import process_image
from keras.utils import np_utils
from typing import List

__author__ = "ujihirokazuya"
__date__ = "2017/10/28"


class DataFileInfo(object):

    def __init__(self, values: list):
        # train,almond,almond,150
        self.train_or_test = values[0]
        self.class_name = values[1]
        self.file_name = values[2]
        self.frame_size = int(values[3])


class DataSet():

    def __init__(self, seq_length: int=40, class_size_limit=None, image_shape=(224, 224, 3)):
        """

        :param seq_length: the number of frames to consider
        :param class_size_limit: number of classes to limit the data to. None is no limit.
        :param image_shape: image shape
        """
        self.seq_length = seq_length
        self.class_size_limit = class_size_limit
        self.max_frames = 300
        self._data_list = self._get_data_list()
        self.class_names = self._get_class_names()
        self._data_list = self._get_valid_data_list()
        self.image_shape = image_shape

    @property
    def data_list(self) -> List[DataFileInfo]:
        return self._data_list

    def split_train_test(self):
        """Split the data into train and test groups."""
        train = list()
        test = list()
        for data_info in self.data_list:
            if data_info.train_or_test == 'train':
                train.append(data_info)
            else:
                test.append(data_info)
        return train, test

    def get_all_sequences_in_memory(self, data_info_list: List[DataFileInfo]):
        """
        This is a mirror of our generator, but attempts to load everything into
        memory so we can train way faster.
        """
        # train, test = self.split_train_test()
        print("Loading {} samples into memory.".format(len(data_info_list)))
        x, y = [], []
        for data_file_info in data_info_list:
            sequence = self._get_sequence_from_data_file_info(data_file_info)
            x.append(sequence)
            y.append(self._get_class_one_hot(data_file_info.class_name))
        return np.array(x), np.array(y)

    def frame_generator(self, batch_size, data_info_list: List[DataFileInfo]):
        print("Creating generator with {} samples." % (len(data_info_list)))
        while 1:
            x, y = [], []
            for _ in range(batch_size):
                sample = random.choice(data_info_list)
                sequence = self._get_sequence_from_data_file_info(sample)
                if sequence is None:
                    raise ValueError("Can't find sequence. Did you generate them?")
                x.append(sequence)
                y.append(self._get_class_one_hot(sample.class_name))
            yield np.array(x), np.array(y)

    @staticmethod
    def _get_data_list() -> List[DataFileInfo]:
        data_list = list()
        with open('./data/data_file.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                data = DataFileInfo(row)
                data_list.append(data)
        return data_list

    def _get_valid_data_list(self):
        valid_data_list = list()
        for data_info in self.data_list:
            if self.seq_length <= data_info.frame_size <= self.max_frames and data_info.class_name in self.class_names:
                valid_data_list.append(data_info)
        return valid_data_list

    def _get_class_names(self):
        classes = list()
        for data_info in self.data_list:
            if data_info.class_name not in classes:
                classes.append(data_info.class_name)
        classes = sorted(classes)
        if self.class_size_limit is not None:
            return classes[:self.class_size_limit]
        return classes

    def _get_class_one_hot(self, class_name):
        class_index = self.class_names.index(class_name)
        label_hot = np_utils.to_categorical(class_index, len(self.class_names))
        label_hot = label_hot[0]  # just get a single row
        return label_hot

    def _get_sequence_from_data_file_info(self, data_file_info: DataFileInfo):
        image_file_names = self._get_image_file_names(data_file_info)
        image_file_names = self._rescale_list(image_file_names, self.seq_length)
        sequence = self._get_sequence_from_image(image_file_names)
        return sequence

    def _get_sequence_from_image(self, image_file_names):
        return [process_image(image_file_path=x, target_shape=self.image_shape, gray_scale=True) for x in
                image_file_names]

    @staticmethod
    def _get_image_file_names(data_info: DataFileInfo):
        directory_path = "./data/{}/{}/".format(data_info.train_or_test, data_info.class_name)
        filename = data_info.file_name
        images = sorted(glob.glob(directory_path + filename + '*jpg'))
        return images

    @staticmethod
    def _get_filename_from_image(filename):
        parts = filename.split('/')
        return parts[-1].replace('.jpg', '')

    @staticmethod
    def _rescale_list(input_list, size):
        assert len(input_list) >= size
        skip = len(input_list) // size
        output = [input_list[i] for i in range(0, len(input_list), skip)]
        return output[:size]

    def print_class_from_prediction(self, predictions, nb_to_return=5):
        """Given a prediction, print the top classes."""
        # Get the prediction for each label.
        label_predictions = {}
        for i, label in enumerate(self.class_names):
            label_predictions[label] = predictions[i]

        # Now sort them.
        sorted_lps = sorted(
            label_predictions.items(),
            key=operator.itemgetter(1),
            reverse=True
        )

        # And return the top N.
        for i, class_prediction in enumerate(sorted_lps):
            if i > nb_to_return - 1 or class_prediction[1] == 0.0:
                break
            print("{}: {}".format(class_prediction[0], class_prediction[1]))
