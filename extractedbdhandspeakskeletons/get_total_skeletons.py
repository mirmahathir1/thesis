import pandas as pd
from os import listdir
from os.path import isfile, join
from tqdm import tqdm

csv_file_root = './subtitles_translated_csv.v2'
csv_file_list = [f for f in listdir(csv_file_root) if isfile(join(csv_file_root, f))]

video_resolutions = dict()

total_duration = 0
total_words = 0
for csv_file_name in tqdm(csv_file_list):
    dataframe = pd.read_csv(f"{csv_file_root}/{csv_file_name}")
    for index, row in dataframe.iterrows():
        words = row["translation"].split(" ")
        for word in words:
            if not len(word) == 0:
                total_words += 1

print(f"total words: {total_words}")
