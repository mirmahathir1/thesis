import crop_video

from os import listdir
from os.path import isfile, join

path_of_raw_videos = "raw_videos"
path_of_cropped_videos = "cropped_videos"

video_names = [f for f in listdir(path_of_raw_videos) if isfile(join(path_of_raw_videos, f))]
# print(video_names)

for video_name in video_names:
    print(path_of_cropped_videos + "/" + video_name)
    if not isfile(path_of_cropped_videos + "/" + video_name):
        crop_video.save_sign_language_video(path_of_raw_videos + "/" + video_name, path_of_cropped_videos)
    else:
        print("Skipping")
