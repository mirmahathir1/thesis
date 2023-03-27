import moviepy.editor as mp
from os import listdir
from os.path import isfile, join
import sys
sys.path.append('../')
import lib

path_of_cropped_videos = "..\\extractedbtvdataset\\cropped_reduced_videos"

video_names = lib.get_file_list_directory(path_of_cropped_videos, '.mp4')
for video_name in video_names:
    audio_file_path = f"mp3_files\\{video_name}.wav"
    video_file_path = f"{path_of_cropped_videos}\\{video_name}.mp4"
    print(f"processing: {video_name}")
    if isfile(audio_file_path):
        print("skipping")
        continue
    clip = mp.VideoFileClip(video_file_path)
    clip.audio.write_audiofile(audio_file_path)
    exit()
