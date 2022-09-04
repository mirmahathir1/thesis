from moviepy.editor import *
from moviepy.video.fx.crop import crop
import ntpath
from os.path import isfile

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def save_sign_language_video(video_path, cropped_path):
    if isfile(cropped_path + "/" + path_leaf(video_path)):
        print("Skipping video "+path_leaf(video_path))
        return

    clip = VideoFileClip(video_path)

    header_trim_duration = 10
    footer_trim_duration = 40

    duration = clip.duration

    (w, h) = clip.size

    # if not (w == 1280 and h == 720):
    #     print("ERROR: Unexpected dimension found")

    # clip = clip.subclip(header_trim_duration, duration - footer_trim_duration)
    # clip = clip.subclip(10, 40)

    cropped_clip = crop(clip, width=2 * w / 5, height=(3*h)/5, x_center=4 * w / 5,
                        y_center=(11*h)/24)

    # print(cropped_path+"/" + path_leaf(video_path))
    cropped_clip.write_videofile(cropped_path + "/" + path_leaf(video_path),
                                 audio_codec='aac', fps=30)

# save_sign_language_video("raw_videos/13m in UK have received vaccine as cases soar 🔴 Boris Johnson Covid Briefings @BBC News live - BBC.mp4", "sample_videos")
