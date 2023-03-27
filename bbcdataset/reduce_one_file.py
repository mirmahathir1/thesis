from moviepy.editor import *
from os.path import isfile
import shutil


def reduce(src_directory, video_file, dst_directory, fps):
    file_name_without_ext = video_file.split(".")[0]
    output_file_path = dst_directory + file_name_without_ext + "_reduced.mp4"

    if isfile(output_file_path):
        print("DUPLICATE: skipping ", output_file_path)
        return

    clip = VideoFileClip(src_directory + video_file)
    print(clip.fps)
    print("generating: ", output_file_path)

    clip = VideoFileClip(src_directory + video_file)
    clip = clip.set_fps(fps)

    clip.write_videofile("./meh.mp4", audio_codec='aac')
    shutil.move('./meh.mp4', output_file_path)

