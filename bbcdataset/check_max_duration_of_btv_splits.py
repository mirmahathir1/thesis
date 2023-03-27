import lib

directory = '../extractedbtvdataset/audio_segments'

list_of_audio_segments = lib.get_file_list_directory(directory, '.txt')

max_duration = 0
min_duration = 9999999999

for single_text_file in list_of_audio_segments:
    name_of_file = f"{directory}/{single_text_file}.txt"
    file_object = open(name_of_file, "r")
    lines_in_file = file_object.read().splitlines()
    file_object.close()

    for single_line in lines_in_file:
        [start_time, end_time] = single_line.split(' ')
        start_time = float(start_time)
        end_time = float(end_time)
        max_duration = max(end_time - start_time, 0)
        min_duration = min(end_time - start_time, min_duration)

print(max_duration)
print(min_duration)
