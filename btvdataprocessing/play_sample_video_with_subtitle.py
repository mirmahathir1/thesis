import pandas as pd
import cv2
from moviepy.editor import *
from moviepy.config import change_settings
import os
change_settings({"IMAGEMAGICK_BINARY": r"C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})

video_root = '../extractedbtvdataset/cropped_reduced_videos'

sentence_dataframe = pd.read_csv('sentences.csv',usecols=['video_name', 'start_time', 'end_time', 'sentence','sentence_id'])

sample_dataframe = sentence_dataframe.sample(50)

final_added_movielist = []

skeleton_point_names = [
    {'name': 'pose', 'count': 25, 'lines':[
    [0,15],[0,16],[15,17],[16,18],[0,1],[1,2],[2,3],[3,4],[1,5],[5,6],[6,7],[1,8],[8,9],[9,10],[10,11],[11,22],[11,24],[22,23],[8,12],[12,13],[13,14],[14,21],[14,19],[19,20]
    ]},
    {'name': 'face', 'count': 70, 'lines':[]},
    {'name': 'hand_left', 'count': 21, 'lines':[
    [0,1],[1,2],[2,3],[3,4],[0,5],[5,6],[6,7],[7,8],[0,9],[9,10],[10,11],[11,12],[0,13],[13,14],[14,15],[15,16],[0,17],[17,18],[18,19],[19,20]
    ]},
    {'name': 'hand_right', 'count': 21, 'lines':[
    [0,1],[1,2],[2,3],[3,4],[0,5],[5,6],[6,7],[7,8],[0,9],[9,10],[10,11],[11,12],[0,13],[13,14],[14,15],[15,16],[0,17],[17,18],[18,19],[19,20]
    ]}
]

for index, row in sample_dataframe.iterrows():
    video_name = row['video_name']
    start_time = float(row['start_time'])
    end_time = float(row['end_time'])
    sentence = row['sentence']
    sentence_id = row['sentence_id']

    print(sentence_id)

    # Load your video
    video = VideoFileClip(f"{video_root}/{video_name}_cropped_reduced.mp4")
    audio = AudioFileClip(f"{video_root}/{video_name}_cropped_reduced.mp4")

    video = video.subclip(start_time, end_time)
    audio = audio.subclip(start_time, end_time)

    skeleton_dataframe = pd.read_csv(f"skeletons_with_sentence_id/{video_name}/{sentence_id}.csv", index_col=0)
    new_frames = []

    skeleton_dataframe_index = 0
    for frame in video.iter_frames():
        frame_copy = frame.copy()
        if skeleton_dataframe_index >= skeleton_dataframe.shape[0]:
            print(f"skeleton count: {skeleton_dataframe.shape[0]}, frame: {video.duration * video.fps}")
            break

        for point in skeleton_point_names:
            for i in range(point['count']):
                x = int(skeleton_dataframe.iloc[skeleton_dataframe_index][f"{point['name']}_{i}_x"])
                y = int(skeleton_dataframe.iloc[skeleton_dataframe_index][f"{point['name']}_{i}_y"])
                cv2.circle(frame_copy, (x, y), 2, (255, 0, 0), -1)

            for line in point['lines']:
                line_start = line[0]
                line_end = line[1]
                skeleton = skeleton_dataframe.iloc[skeleton_dataframe_index]
                x_start = int(skeleton[f"{point['name']}_{line_start}_x"])
                y_start = int(skeleton[f"{point['name']}_{line_start}_y"])
                x_end = int(skeleton[f"{point['name']}_{line_end}_x"])
                y_end = int(skeleton[f"{point['name']}_{line_end}_y"])


                if x_start == 0 or y_start == 0 or x_end == 0 or y_end == 0:
                    continue

                cv2.line(frame_copy, (x_start, y_start), (x_end, y_end), (0, 0, 255), 1)

        new_frames.append(frame_copy)
        skeleton_dataframe_index = skeleton_dataframe_index + 1

    video_with_point = ImageSequenceClip(new_frames, fps=10)
    video_with_point.audio = audio

    # Create a TextClip
    text = TextClip(sentence, font="SolaimaniLipi", fontsize=15, color='white', size = (video.w, 100), method='caption')

    text = text.set_duration(video.duration)

    # Set the position of the TextClip
    text = text.set_position(('center', 'bottom'))

    # Overlay the TextClip on the video
    clip_with_text = CompositeVideoClip([video_with_point, text])

    final_added_movielist.append(clip_with_text)

final_clip = concatenate_videoclips(final_added_movielist)

final_clip.write_videofile('my_video_with_text.mp4', fps = 10)

os.startfile('my_video_with_text.mp4')
