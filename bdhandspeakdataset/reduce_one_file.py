from moviepy.editor import *
from os.path import isfile


def reduce(src_directory, video_file, dst_directory, fps):
    file_name_without_ext = video_file.split(".")[0]

    if isfile(dst_directory + file_name_without_ext + ".mp4"):
        print("DUPLICATE: skipping ", dst_directory + file_name_without_ext + ".mp4")
        return

    # print(clip.w, " ", clip.h)

    print("generating: ", dst_directory + file_name_without_ext + ".mp4")

    clip = VideoFileClip(src_directory + video_file)
    print("source: "+src_directory + video_file)
    clip = clip.set_fps(fps)

    clip.write_videofile(dst_directory + file_name_without_ext + ".mp4",
                         audio_codec='aac')
