import lib
from moviepy.editor import *

total_seconds = 0

audio_root_path = "../extractedbtvdataset/extracted_audio_segments"

for video_path in lib.get_file_list_directory_recurse("../extractedbtvdataset/segmented_videos",".mp4"):
    clip = VideoFileClip(video_path)
    [root, folder, video_name] = video_path.split('\\')
    # print(root, folder, video_name)
    video_name_with_modified_extension= video_name.replace(".mp4", ".mp3")
    mp3_file_path = f"{audio_root_path}/{folder}/{video_name_with_modified_extension}"
    lib.makedir(f"{audio_root_path}/{folder}")
    clip.audio.write_audiofile(mp3_file_path)
    clip.close()
