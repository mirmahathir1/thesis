import lib
from moviepy.editor import *

selected_video_path = "../extractedbtvdataset/cropped_reduced_videos"
audio_segment_text_root_path = "../extractedbtvdataset/audio_segments"
video_list = lib.get_file_list_directory(selected_video_path,'.mp4')

for video_name in video_list:
    video_path = f"{selected_video_path}/{video_name}.mp4"
    audio_segment_duration_text_file_path = f"{audio_segment_text_root_path}/{video_name}_segmentationfile.txt"

    audio_segment_file_object = open(audio_segment_duration_text_file_path, 'r')

    print(f"starting: {video_path}")
    clip = VideoFileClip(video_path)
    folder_for_segmentations = f"segmented_videos/{video_name}"
    lib.makedir(folder_for_segmentations)
    for line in audio_segment_file_object.readlines():
        durations = line.split()
        start_time = float(durations[0])
        end_time = float(durations[1])

        segmented_video_path = f"{folder_for_segmentations}/{video_name}_{start_time:.4f}_{end_time:.4f}.mp4"

        if lib.exists(segmented_video_path):
            print(f"skip: {segmented_video_path}")
            continue
        print(f"processing: {segmented_video_path}")
        audio_segment_clip = clip.subclip(start_time, end_time)

        audio_segment_clip.write_videofile(f"tmp/tmp.mp4", codec='libx264')
        lib.move("tmp/tmp.mp4", segmented_video_path)
        audio_segment_clip.close()

    audio_segment_file_object.close()
    clip.close()
