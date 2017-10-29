# -*- coding: utf-8 -*-
import csv
import glob
import os
import os.path
from subprocess import call

__author__ = "ujihirokazuya"
__date__ = "2017/10/28"


_video_extension = "mp4"
_picture_extension = "jpg"


class VideoPathInfo(object):

    _path_delimiter = "/"
    _movie_path_pattern = "{}/{}/{}"
    _picture_path_pattern = "{}/{}/{}{}"

    def __init__(self, video_path: str):
        parts = video_path.split(self._path_delimiter)
        self.train_or_test = parts[1]
        self.class_name = parts[2]
        self.filename = parts[3]
        self.filename_no_extension = self.filename.split(".")[0]

    def create_movie_path(self):
        return self._movie_path_pattern.format(self.train_or_test, self.class_name, self.filename)

    def create_picture_path(self, extension: str):
        return self._picture_path_pattern.format(self.train_or_test, self.class_name, self.filename_no_extension,
                                                 extension)


def extract_files():
    """
    We'll first need to extract images from each of the videos. We'll
    need to record the following data in the file:
    [train|test], class, filename, nb frames

    Extracting can be done with ffmpeg:
    `ffmpeg -i video.mpg image-%04d.jpg`
    """
    data_file = []
    folders = ['./train/', './test/']
    for folder in folders:
        class_folders = glob.glob(folder + '*')
        for video_class in class_folders:
            video_path_list = glob.glob("{}/*.{}".format(video_class, _video_extension))
            for video_path in video_path_list:
                video_path_info = VideoPathInfo(video_path)
                if not check_already_extracted(video_path_info):
                    # Now extract it.
                    movie_path = video_path_info.create_movie_path()
                    picture_path = video_path_info.create_picture_path("-%04d." + _picture_extension)
                    call(["ffmpeg", "-i", movie_path, "-t", "5", picture_path])
                frame_size = get_frame_size_for_video(video_path_info)
                data_file.append([video_path_info.train_or_test,
                                  video_path_info.class_name,
                                  video_path_info.filename_no_extension,
                                  frame_size])
                print("Generated {} frames for {}".format(frame_size, video_path_info.filename_no_extension))

    with open('data_file.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(data_file)
    print("Extracted and wrote {} video files.".format(len(data_file)))


def get_frame_size_for_video(video_path_info: VideoPathInfo):
    generated_files = glob.glob(video_path_info.create_picture_path("*." + _picture_extension))
    return len(generated_files)


def check_already_extracted(video_path_info: VideoPathInfo):
    return os.path.exists(video_path_info.create_picture_path("-0001." + _picture_extension))


def main():
    """
    Extract images from videos and build a new file that we
    can use as our data input file. It can have format:

    [train|test], class, filename, nb frames
    """
    extract_files()


if __name__ == '__main__':
    main()
