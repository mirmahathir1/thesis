import pandas as pd
from moviepy.editor import *
import lib
video_root = '../extractedbtvdataset/cropped_reduced_videos'

sentence_dataframe = pd.read_csv('sentences.csv',usecols=['sentence_id', 'video_name', 'start_time', 'end_time', 'sentence'])

video_list = sentence_dataframe['video_name'].unique()

print(video_list)

skeleton_csv_root = '../extractedbtvdataset/csv_files_of_skeletons'

lib.makedir('skeletons_with_sentence_id')

for index, video in enumerate(video_list):
    print(index)
    skeleton_dataframe = pd.read_csv(f"{skeleton_csv_root}/{video}_cropped_reduced.csv", index_col=0)
    sentences_of_single_video = sentence_dataframe[sentence_dataframe['video_name'] == video]
    lib.makedir(f"skeletons_with_sentence_id/{video}")
    for index, row  in sentences_of_single_video.iterrows():
        sentence_id= row['sentence_id']
        start_frame_index = int(row['start_time']*10)
        end_frame_index = int(row['end_time'] * 10)
        skeletons_of_single_sentence = skeleton_dataframe.iloc[start_frame_index:end_frame_index]
        skeletons_of_single_sentence.reset_index(drop=True).to_csv(f"skeletons_with_sentence_id/{video}/{sentence_id}.csv")
