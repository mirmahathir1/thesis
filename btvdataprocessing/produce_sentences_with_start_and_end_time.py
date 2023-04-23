import lib
import pandas as pd
import traceback
import os
text_with_end_of_line_directory = "../extractedbtvdataset/text_lines_WITHENDOFLINE"
words_with_timestamp = "../extractedbtvdataset/word_timestamps"

list_of_videos = lib.get_folder_list_directory(text_with_end_of_line_directory)

lib.makedir('sentences_with_time')

for video in list_of_videos:
    list_of_segments_in_video = lib.get_file_list_directory(f"{text_with_end_of_line_directory}/{video}",'.txt')
    lib.makedir(f"sentences_with_time/{video}")
    for single_segment in list_of_segments_in_video:
        sentence_file_location = f"{text_with_end_of_line_directory}/{video}/{single_segment}.txt"
        timestamp_file_location = f"{words_with_timestamp}/{video}/{single_segment}.csv"

        text_file_with_end_of_line = open(sentence_file_location, encoding='utf-8')
        word_timestamp_dataframe = pd.read_csv(timestamp_file_location,usecols=['word', 'start_time', 'end_time'])

        seperate_sentences = lib.read_lines_from_file_object(text_file_with_end_of_line)

        sentence_with_start_and_end_file_path = f"sentences_with_time/{video}/{single_segment}.csv"

        if lib.exists(sentence_with_start_and_end_file_path):
            continue
        print(f"processing: {single_segment}")
        
        transcript_dataframe = pd.DataFrame(columns=['start_time', 'end_time', 'sentence'])
        sentences_word_level= []
        for sentence in seperate_sentences:
            sentences_word_level.append(sentence.split())
        
        try:
            active_sentence_index = 0
            active_sentence_word_index = 0
            active_sentence_start_time = 0
            for index, row in word_timestamp_dataframe.iterrows():
                current_word_start_time = row['start_time']
                current_word_end_time = row['end_time']
                current_word = row['word']

                if active_sentence_word_index == 0:
                    active_sentence_start_time = current_word_start_time

                if not current_word == sentences_word_level[active_sentence_index][active_sentence_word_index]:
                    print(f"current word in timestamp file: {current_word}")
                    print(f"current word in continuous sentence: {sentences_word_level[active_sentence_index][active_sentence_word_index]}")
                    print(f"fatal error. word did not match")
                    os.startfile(sentence_file_location.replace('/',"\\"))
                    os.startfile(timestamp_file_location.replace('/',"\\"))
                    exit(0) 
                active_sentence_word_index = active_sentence_word_index + 1

                if active_sentence_word_index == len(sentences_word_level[active_sentence_index]):
                    new_row = pd.DataFrame({
                    'start_time': active_sentence_start_time,
                    'end_time': current_word_end_time,
                    'sentence': " ".join(sentences_word_level[active_sentence_index]),
                    }, index=[0])
                    transcript_dataframe = pd.concat([transcript_dataframe.loc[:],new_row]).reset_index(drop=True)
                    active_sentence_index = active_sentence_index + 1
                    active_sentence_word_index = 0

            transcript_dataframe.to_csv(sentence_with_start_and_end_file_path, index=False)

            text_file_with_end_of_line.close()
        except:
            traceback.print_exc()
            exit()
