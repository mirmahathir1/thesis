import lib
from moviepy.editor import *

total_seconds = 0


for video_path in lib.get_file_list_directory_recurse("../extractedbtvdataset/segmented_videos",".mp4"):
    clip = VideoFileClip(video_path)
    print(video_path)
    total_seconds = total_seconds + clip.duration

print(f"total minute: {total_seconds/60}")
