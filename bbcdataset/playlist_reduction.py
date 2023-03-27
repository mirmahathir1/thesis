import reduce_one_file

from os import listdir
from os.path import isfile, join
import sys
sys.path.append('../')
import lib


path_of_cropped_videos = "../extractedbtvdataset/cropped_videos/"
path_of_reduced_videos = "../extractedbtvdataset/cropped_reduced_videos/"

video_names = lib.get_file_list_directory(path_of_cropped_videos, '.mp4')

for video_name in video_names:
    reduce_one_file.reduce(path_of_cropped_videos, f"{video_name}.mp4", path_of_reduced_videos, 10)
