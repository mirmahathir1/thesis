import reduce_one_file

from os import listdir
from os.path import isfile, join


path_of_cropped_videos = "cropped_videos/"
path_of_reduced_videos = "reduced_videos/"

video_names = [f for f in listdir(path_of_cropped_videos) if isfile(join(path_of_cropped_videos, f))]
video_names = [video for video in video_names if '.mp4' in video]
# print(video_names)

for video_name in video_names:
    print(path_of_cropped_videos + "/" + video_name)
    reduce_one_file.reduce(path_of_cropped_videos, video_name, path_of_reduced_videos, 10)
