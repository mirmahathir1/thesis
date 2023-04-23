import pandas as pd

dataframe = pd.read_csv('sentences.csv')

total_seconds = 0
all_words = []
for index,row in dataframe.iterrows():
    start_time = float(row['start_time'])
    end_time = float(row['end_time'])
    total_seconds = total_seconds + (end_time - start_time)
    sentence = row['sentence']
    all_words = all_words + sentence.split(' ')

print(f"total seconds: {total_seconds}")
print(f"total words: {len(all_words)}")
print(f"unique words: {len(set(all_words))}")
