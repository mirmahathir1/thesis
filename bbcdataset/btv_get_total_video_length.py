from os import listdir, walk
from os.path import isfile, join
from moviepy.editor import *
import lib

path_of_reduced_videos = "raw_videos/cropped_videos"

list_of_videos = lib.get_file_list_directory(path_of_reduced_videos,'.mp4')
total_seconds = 0


for video_name in list_of_videos:
    video_file_path = f"{path_of_reduced_videos}/{video_name}.mp4"
    clip = VideoFileClip(video_file_path)
    print(clip.duration)
    total_seconds = total_seconds + clip.duration

print(f"total hour: {total_seconds/3600}")
