import lib
from moviepy.editor import *
from ast import literal_eval as make_tuple
from moviepy.video.fx.all import crop
from moviepy.video.fx.all import resize
import shutil
import math


base_video_folder = 'raw_videos/selected'
video_names = lib.get_file_list_directory(base_video_folder,'.mp4')
base_coordinate_folder = 'raw_videos/selected_coordinates'

for video_name in video_names:
    print("video name: ", video_name)
    video_file_name = f"{base_video_folder}/{video_name}.mp4"
    coordinate_file_name = f"{base_coordinate_folder}/{video_name}_coordinates.txt"
    cropped_video_name = f"raw_videos/cropped_videos/{video_name}_cropped.mp4"

    if lib.exists(cropped_video_name):
        print("file already cropped")
        continue

    clip = VideoFileClip(video_file_name)
    print("duration: ", clip.duration)

    coordinate_file_object = open(coordinate_file_name)
    (xmin, xmax, ymin, ymax) = make_tuple(coordinate_file_object.readline())
    xmin = math.ceil(xmin)
    ymin = math.ceil(ymin)
    ymax = math.floor(ymax)
    xmax = math.floor(xmax)
    print("coordinates: ", xmin, xmax, ymin, ymax)
    coordinate_file_object.close()

    cropped_clip = crop(clip,x1 = xmin, y1=ymin, x2=xmax, y2=ymax)
    resized_clip = resize(cropped_clip, newsize=(300,300))

    resized_clip.write_videofile('tmp/meh.mp4',codec='libx264')
    shutil.move("tmp/meh.mp4", cropped_video_name)
