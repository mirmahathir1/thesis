import shutil
import os
from os import listdir
from os.path import isfile, join
import numpy as np
import json
import re
import pandas as pd

properties_of_consideration = [{
    'name': 'pose_keypoints_2d', 'count': 25
}, {
    'name': 'face_keypoints_2d', 'count': 70
}, {
    'name': 'hand_left_keypoints_2d', 'count': 21
}, {
    'name': 'hand_right_keypoints_2d', 'count': 21
}]


column_names = []

total_body_keypoint_count = 0
for property in properties_of_consideration:
    property_name = "_".join(property['name'].split('_')[:-2])
    for i in range(property['count']):
        column_names.append(f"{ property_name }_{i}_x")
        column_names.append(f"{ property_name }_{i}_y")
    total_body_keypoint_count += property['count']

def add_column(df, row):
    if len(row) != len(column_names):
        print(f"{len(row)} {len(column_names)}")
        print("fatal error. inserted list length not matched with dataframe column count")
        exit(1)
    df.loc[len(df.index)] = row

path_to_jsons = "./extracted_skeletons"

# path_to_zips = '../extractedbdhandspeakskeletons/jsons'
path_to_zips = '../extractedbbcskeletons/jsons'

zip_files = [f for f in listdir(path_to_zips) if isfile(join(path_to_zips, f))]

for zip_file_name in zip_files:
    print(f"processing zip file: {zip_file_name}")

    if isfile(f"./csv_files/{zip_file_name.split('.')[0]}.csv"):
        print(f"skipping: {zip_file_name}")
        continue

    shutil.rmtree('./extracted_skeletons', ignore_errors=True)
    os.makedirs('./extracted_skeletons', exist_ok=True)
    filename = path_to_zips+"/"+zip_file_name
    extract_dir = "./extracted_skeletons"
    archive_format = "zip"
    shutil.unpack_archive(filename, extract_dir, archive_format)

    json_data_frame = pd.DataFrame(columns=column_names)
    json_list = [f for f in listdir(path_to_jsons) if isfile(join(path_to_jsons, f))]
    json_list.sort(key=lambda f: int(re.sub('\D', '', f)))

    for json_file_name in json_list:
        f = open(path_to_jsons+'/'+json_file_name)
        data = json.load(f)

        if len(data['people']) == 0:
            add_column(json_data_frame, np.zeros(total_body_keypoint_count*2))
            continue

        max_sum_of_probablities = 0
        most_probable_person = None
        for person in data['people']:
            probability_sum = 0
            for property in properties_of_consideration:
                probability_sum += sum(person[property['name']][2::3])
            if probability_sum > max_sum_of_probablities:
                max_sum_of_probablities = probability_sum
                most_probable_person = person

        dataframe_row = []
        for property in properties_of_consideration:
            column_prefix = "_".join(property['name'].split('_')[:-2])
            x_cordinates = most_probable_person[property['name']][0::3]
            y_cordinates = most_probable_person[property['name']][1::3]
            for i in range(property['count']):
                dataframe_row.append(x_cordinates[i])
                dataframe_row.append(y_cordinates[i])
        
        add_column(json_data_frame, dataframe_row)

    json_data_frame.to_csv(f"./csv_files/{zip_file_name.split('.')[0]}.csv")
