import reduce_one_file

from os import listdir, walk
from os.path import isfile, join
from moviepy.editor import *

path_of_reduced_videos = "reduced_videos\\"

# print(video_names)

video_names = []

for path, subdirs, files in walk('videos'):
    for name in files:
        file_path = join(path, name)  # change to your own video path
        if '.mp4' not in file_path or 'ignore' in file_path:
            continue
        print(file_path)
        video_names.append(file_path)

total_seconds = 0
for video_name in video_names:
    print("" + video_name)
    clip = VideoFileClip(video_name)
    print(clip.duration)
    total_seconds = total_seconds + clip.duration

print(f"total hour: {total_seconds/3600}")
