import moviepy.editor as mp
from os import listdir
from os.path import isfile, join

path_of_cropped_videos = "..\\extractedbbcskeletons\\reduced_framerate_raw_videos"
video_names = [f for f in listdir(path_of_cropped_videos) if isfile(join(path_of_cropped_videos, f))]
for video_name in video_names:
    audio_file_path = f"mp3_files\\{video_name}.mp3"
    video_file_path = f"..\\extractedbbcskeletons\\reduced_framerate_raw_videos\\{video_name}"
    print(f"processing: {video_name}")
    if isfile(audio_file_path):
        print("skipping")
        continue
    clip = mp.VideoFileClip(video_file_path)
    clip.audio.write_audiofile(audio_file_path)
