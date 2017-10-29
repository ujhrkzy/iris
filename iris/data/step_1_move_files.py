# -*- coding: utf-8 -*-
import os
import os.path

__author__ = "ujihirokazuya"
__date__ = "2017/10/28"


def get_data_list(version: str='01'):
    test_file = './data_list/test_list' + version + '.txt'
    train_file = './data_list/train_list' + version + '.txt'

    # Build the test list.
    with open(test_file) as fin:
        test_list = [row.strip() for row in list(fin)]

    # Build the train list. Extra step to remove the class index.
    with open(train_file) as fin:
        train_list = [row.strip().split(" ")[0] for row in list(fin)]

    # Set the groups in a dictionary.
    file_groups = {
        'train': train_list,
        'test': test_list
    }
    return file_groups


def move_files(file_groups: dict):
    for group, video_path_list in file_groups.items():
        for video_path in video_path_list:
            parts = video_path.split('/')
            video_class_name = parts[0]
            filename = parts[1]
            directory_name = os.path.join(group, video_class_name)
            if not os.path.exists(directory_name):
                print("Creating folder for {}".format(directory_name))
                os.makedirs(directory_name)
            if not os.path.exists(filename):
                print("Can't find {} to move. Skipping.".format(filename))
                continue
            new_file_path = os.path.join(directory_name, filename)
            print("Moving {} to {}".format(filename, new_file_path))
            os.rename(filename, new_file_path)
    print("Done.")


def main():
    """
    Go through each of our train/test text files and move the videos
    to the right place.
    """
    # Get the videos in groups so we can move them.
    group_lists = get_data_list()

    # Move the files.
    move_files(group_lists)


if __name__ == '__main__':
    main()
