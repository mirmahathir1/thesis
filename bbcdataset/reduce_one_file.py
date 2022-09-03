from moviepy.editor import *
from moviepy.video.fx.all import blackwhite, resize
from os.path import isfile, join
import config


def reduce(src_directory, video_file, dst_directory, fps):

    file_name_without_ext = video_file.split(".")[0]

    if isfile(dst_directory + file_name_without_ext + ".mp4"):
        print("DUPLICATE: skipping ", dst_directory + file_name_without_ext + ".mp4")
        return

    clip = VideoFileClip(src_directory + video_file)

    print(clip.fps)
    # print(clip.w, " ", clip.h)

    original_video = VideoFileClip(src_directory + video_file)

    print("generating: ", dst_directory + file_name_without_ext + ".mp4")



    clip = VideoFileClip(src_directory + video_file)
    # clip = clip.resize(dimension)
    clip = clip.set_fps(fps)

    clip.write_videofile(dst_directory + file_name_without_ext + ".mp4",
                                 audio_codec='aac')


reduce("cropped_videos/", "Ill be getting the AstraZeneca jab tomorrow Boris Johnson @BBC News live 🔴 BBC.mp4", "reduced_videos/",
    10)
