from cmath import isnan
from re import sub
from moviepy.editor import *

from os import listdir
from os.path import isfile, join
import pandas as pd
import json
import numpy as np
from tqdm import tqdm

json_indentation = None
# json_indentation = 4

raw_video_path_root = '../extractedbdhandspeakskeletons/reduced_framerate_raw_videos'
subtitle_csv_file_path_root = '../extractedbdhandspeakskeletons/subtitles_translated_csv.v2'
skeleton_csv_file_path_root = '../extractedbdhandspeakskeletons/skeleton_csv'

json_file_path_root = '../extractedbdhandspeakskeletons/skeleton_subtitle_jsons'

raw_video_paths = [f for f in listdir(raw_video_path_root) if isfile(join(raw_video_path_root, f))]

for video_file in tqdm(raw_video_paths):
    # print(f"reading video {video_file}")
    video_name = video_file.split('.')[0]

    video_full_path = raw_video_path_root+"/"+video_file
    subtitle_csv_full_path = subtitle_csv_file_path_root + "/" + video_name + '.txt.csv'
    skeleton_csv_full_path = skeleton_csv_file_path_root + "/" + video_name.strip() + '.csv'
    
    clip = VideoFileClip(video_full_path)
    subtitle_dataframe = pd.read_csv(subtitle_csv_full_path, index_col=0)
    skeleton_dataframe = pd.read_csv(skeleton_csv_full_path, index_col=0)

    height = clip.size[1]
    width = clip.size[0]
    if height == 0:
        print("video found with zero height. Program will")
        exit(0)
    duration = clip.duration

    center_x = skeleton_dataframe['pose_1_x'].copy(deep=True)
    x_columns = (skeleton_dataframe.filter(like='_x').sub(skeleton_dataframe['pose_1_x'], axis='rows')/height).round(5)

    center_y = skeleton_dataframe['pose_1_y'].copy(deep=True)
    y_columns = (skeleton_dataframe.filter(like='_y').sub(skeleton_dataframe['pose_1_y'], axis='rows')/height).round(5)

    skeleton_dataframe = pd.concat([x_columns, y_columns], axis=1)

    skeleton_dataframe = skeleton_dataframe.fillna(0)

    # print(f"video resolution: {width}X{height}")
    # print(f"subtitle row count: {subtitle_dataframe.shape[0]}")
    # print(f"skeleton file row count: {skeleton_dataframe.shape[0]}")

    subtitle_dataframe = subtitle_dataframe.reset_index()
    skeleton_dataframe = skeleton_dataframe.reset_index()



    skeleton_data = []

    if subtitle_dataframe.shape[0] == 0:
        print(f"no subtitle found for video. code will exit")
        exit(0)

    if skeleton_dataframe.shape[0] == 0:
        print(f"no skeletons found")
        exit(0)

    for index, row in subtitle_dataframe.iterrows():
        single_text_data = dict()
        single_text_data['start_time'] = row['start']
        single_text_data['end_time'] = row['end']
        try:
            single_text_data['english'] = row['text'].strip()
        except:
            print(f"fload: {row['text']}")
            exit(0)
        single_text_data['bengali'] = row['translation'].strip()

        skeleton_start_index = row['start'] * 10
        skeleton_end_index = (row['end'] + 1) * 10

        skeletons = []

        skeleton_subset_dataframe = skeleton_dataframe.iloc[skeleton_start_index:skeleton_end_index]

        if skeleton_subset_dataframe.shape[0] == 0:
            continue


        for skeleton_index, skeleton_row in skeleton_subset_dataframe.iterrows():
            skeletons.append(skeleton_row.to_dict())
        
        single_text_data['skeletons'] = skeletons

        skeleton_data.append(single_text_data)

    if len(skeleton_data) == 0:
        print(f"file found with no skeleton data. code will exit")
        exit(0)

    json_dictionary = dict()
    json_dictionary['video_name'] = video_name
    json_dictionary['duration'] = duration
    json_dictionary['height'] = height
    json_dictionary['width'] = width
    json_dictionary["skeleton_data"] = skeleton_data

    with open(f"{json_file_path_root}/{video_name}.json", "w", encoding="utf-8") as outfile:
        json.dump(json_dictionary, outfile, indent = json_indentation, ensure_ascii=False)
    
    clip.close()
