import moviepy.editor as mp
from pyannote.audio import Pipeline
import hugging_face_token
import math
import sys
sys.path.append('../')
from lib import exists, get_file_list_directory


pipeline = Pipeline.from_pretrained("pyannote/voice-activity-detection", use_auth_token=hugging_face_token.get_token())

video_directory = "../extractedbtvdataset/cropped_reduced_videos"
wav_directory = "./wav_files"
audio_segment_file_directory = "./audio_segments"

video_names = get_file_list_directory(video_directory, '.mp4')

for video_name in video_names:
    print(f"processing video: {video_name}")

    video_file_path = f"{video_directory}/{video_name}.mp4"
    wav_file_path = f"{wav_directory}/{video_name}.wav"
    audio_segment_file_path = f"{audio_segment_file_directory}/{video_name}_segmentationfile.txt"

    if exists(audio_segment_file_path):
        print("skipping")
        continue

    clip = mp.VideoFileClip(video_file_path)
    clip.audio.write_audiofile(wav_file_path)

    print("detecting audio segments")

    output = pipeline(wav_file_path)

    audio_segment_file_object = open(audio_segment_file_path, "w")

    for speech in output.get_timeline().support():
        print(f"{speech.start} {speech.end}", file=audio_segment_file_object)
    
    audio_segment_file_object.close()
