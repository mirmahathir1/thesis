from difflib import SequenceMatcher
import re
import pandas as pd
from os import listdir
from os.path import isfile, join

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def remove_punctuation(sentence):
    sentence = sentence.replace('\'s ', "s ")
    sentence = sentence.replace('\'t ', "t ")
    return re.sub(r'[^\w\s]', ' ', sentence)


def remove_multiple_whitespaces(sentence):
    sentence = sentence.replace('\n','')
    return re.sub(' +', ' ', sentence)


def convert_to_small_letter(sentence):
    return sentence.lower()

path_to_text_files = '../extractedbdhandspeakskeletons/texts'
text_files = [f for f in listdir(path_to_text_files) if isfile(join(path_to_text_files, f))]

for text_file_name in text_files:
    print(f"processing: {text_file_name}")
    text_file = open(path_to_text_files+'/'+text_file_name, 'r')
    lines = text_file.readlines()
    text_file.close()

    base_line_index = 0
    similarity_threshold = 0.9

    line_object_array = []

    for line in lines:
        if len(remove_multiple_whitespaces(line)) == 0:
            break
        infos = line.split('||')
        if len(infos) == 1:
            clean_line = ''
            time = int(infos[0][:-2])
        else:
            clean_line = remove_multiple_whitespaces(remove_punctuation(convert_to_small_letter(infos[0])))
            time = int(infos[1][:-3])

        line_object_array.append({
            'line':clean_line,
            'group':-1,
            'time': time
        })

    current_active_group = 0

    individual_sentences_detected = []

    while True:
        if base_line_index >= len(line_object_array):
            break

        base_line = line_object_array[base_line_index]['line']

        matched_line_array = []
        for i in range(base_line_index,len(line_object_array)):
            similarity = similar(line_object_array[i]['line'],base_line)
            if similarity < similarity_threshold:
                break
            matched_line_array.append({
                'index':i,
                'similarity': similarity
            })
        
        max_index_of_matched = matched_line_array[-1]['index']

        longest_line = ''
        for i in range(base_line_index, max_index_of_matched + 1):
            line_object_array[i]['group'] = current_active_group
            if len(longest_line) < len(line_object_array[i]['line']):
                longest_line = line_object_array[i]['line']

        individual_sentences_detected.append({
            'line': longest_line,
            'start': line_object_array[base_line_index]['time'],
            'end': line_object_array[max_index_of_matched]['time']
        })

        current_active_group += 1

        base_line_index = max_index_of_matched + 1

    cleaned_line_data_frame = pd.DataFrame(columns=['start','end','text'])
    for individual_sentence in individual_sentences_detected:
        cleaned_line_data_frame.loc[len(cleaned_line_data_frame.index)] = [individual_sentence['start'], individual_sentence['end'], individual_sentence['line']]

    cleaned_line_data_frame.to_csv(f"cleaned_texts/{text_file_name}.csv")
