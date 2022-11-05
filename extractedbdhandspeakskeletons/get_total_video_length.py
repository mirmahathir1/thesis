from moviepy.editor import *

from os import listdir
from os.path import isfile, join

mypath = './reduced_framerate_raw_videos'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

video_resolutions = dict()

total_duration = 0
for video_file in onlyfiles:
    print(f"reading video {video_file}")
    clip = VideoFileClip(mypath+"/"+video_file)

    height = clip.size[0]
    width = clip.size[1]
    if height == 0:
        print("video found with zero height. Program will")
        exit(0)
    if f"{height}x{width}" in video_resolutions:
        video_resolutions[f"{height}x{width}"] += 1
    else:
        video_resolutions[f"{height}x{width}"] = 1
    # duration in seconds
    total_duration += clip.duration
    clip.close()

print(f"total duration: {total_duration} seconds")
print(f"total duration: {total_duration/60} minutes")
print(f"total duration: {total_duration/3600} hours")
print(video_resolutions)
