import lib
import pandas as pd
sentences_with_start_end_root = "../extractedbtvdataset/sentences_with_start_end_time"

list_of_folders = lib.get_folder_list_directory(sentences_with_start_end_root)

lib.makedir('sentences_start_end_wrt_raw')

final_dataframe = pd.DataFrame(columns=['sentence_id', 'video_name', 'start_time', 'end_time', 'sentence'])

def addToDataframe(sentence_id, video_name, start_time, end_time, sentence):
    global final_dataframe
    new_row = pd.DataFrame({
        'sentence_id': sentence_id,
        'video_name': video_name,
        'start_time': start_time,
        'end_time': end_time,
        'sentence': sentence,
    }, index=[0])
    final_dataframe = pd.concat([final_dataframe.loc[:],new_row]).reset_index(drop=True)

for folder in list_of_folders:
    video_name = folder.replace('_cropped_reduced','')
    print(video_name)
    video_segments = lib.get_file_list_directory(f"{sentences_with_start_end_root}/{folder}",'.csv')
    for single_segment in video_segments:
        single_segment_start_end = single_segment.split('_cropped_reduced_')[-1].split('_')
        single_segment_start_time = float(single_segment_start_end[0])
        single_segment_end_time = float(single_segment_start_end[1])
        single_segment_csv_path = f"{sentences_with_start_end_root}/{folder}/{single_segment}.csv"
        single_segment_dataframe = pd.read_csv(single_segment_csv_path, usecols=['start_time', 'end_time', 'sentence'])
        
        for index, row in single_segment_dataframe.iterrows():
            sentence_start_time_wrt_segment = float(row['start_time'])

            # end time with slight adjustment
            sentence_end_time_wrt_segment = float(row['end_time']) + 0.5
            bangla_sentence = row['sentence']

            sentence_start_time_wrt_raw = '{:.4f}'.format(single_segment_start_time + sentence_start_time_wrt_segment)
            sentence_end_time_wrt_raw = '{:.4f}'.format(single_segment_start_time + sentence_end_time_wrt_segment)

            sentence_id = f"{video_name}$${sentence_start_time_wrt_raw}$${sentence_end_time_wrt_raw}$$"

            addToDataframe(sentence_id, video_name, sentence_start_time_wrt_raw, sentence_end_time_wrt_raw, bangla_sentence)

final_dataframe.to_csv('sentences.csv', index=False)
