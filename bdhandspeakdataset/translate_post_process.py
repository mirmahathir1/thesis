import pandas as pd
from os import listdir
from os.path import isfile, join
import re
from tqdm import tqdm

def remove_multiple_whitespaces(sentence):
    return re.sub(' +', ' ', sentence)

def remove_english_letters(sentence):
    return re.sub(r'[a-zA-Z]+', '', sentence)

bangla_digits = [str(chr(i)) for i in range(0x09E6,0x09F0,1)]

def replace_english_digits(sentence):
    for english_digit in range(10):
        sentence = re.sub(str(english_digit), str(bangla_digits[english_digit]), sentence)    
    return sentence

path_to_csv_files = '../extractedbdhandspeakskeletons/subtitles_translated_csv'
path_to_post_processed_csv_files = '../extractedbdhandspeakskeletons/subtitles_translated_csv.v2'
csv_files = [f for f in listdir(path_to_csv_files) if isfile(join(path_to_csv_files, f))]

total_lines = 0

for csv_file in tqdm(csv_files):
    data_frame = pd.read_csv(path_to_csv_files + '/' + csv_file)
    data_frame.drop('Unnamed: 0.1', inplace=True, axis=1)
    data_frame.rename(columns={"Unnamed: 0": "index"}, inplace=True)

    total_lines += data_frame.shape[0]

    for index in data_frame.index:
        if pd.isnull(data_frame.loc[index,'translation']) or len(data_frame.loc[index,'translation'].strip()) == 0:
            data_frame.loc[index,'translation'] = 'ফাঁকা'
        if pd.isnull(data_frame.loc[index,'text']) or len(data_frame.loc[index,'text'].strip()) == 0:
            data_frame.loc[index,'text'] = 'silent'

        data_frame.loc[index,'translation'] = replace_english_digits(remove_english_letters(data_frame.loc[index,'translation']))

        if pd.isnull(data_frame.loc[index,'translation']) or len(data_frame.loc[index,'translation'].strip()) == 0:
            data_frame.loc[index,'translation'] = 'ফাঁকা'

    data_frame.to_csv(path_to_post_processed_csv_files + '/' + csv_file, index=False)

print(f"total lines: {total_lines}")
