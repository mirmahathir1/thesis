from moviepy.editor import *

from os import listdir
from os.path import isfile, join

mypath = './reduced_framerate_raw_videos'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

total_duration = 0
for video_file in onlyfiles:
    print(f"reading video {video_file}")
    clip = VideoFileClip(mypath+"/"+video_file)
    # duration in seconds
    total_duration += clip.duration

print(f"total duration: {total_duration} seconds")
print(f"total duration: {total_duration/60} minutes")
print(f"total duration: {total_duration/3600} hours")

# clip = VideoFileClip("dsa_geek.webm")