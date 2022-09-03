with open('transcription.txt') as f:
    lines = f.readlines()

cleaned_lines = ' '.join([line.strip().replace('\n', '') for line in lines]).split('%%')

unique_lines = []
valid_lines = []
unique_lines_with_info = []
video_end_time = 0

for line in cleaned_lines:
    line_splits = line.split('||')
    if not len(line_splits) == 2:
        continue
    main_content_cleaned = line_splits[0].strip()
    cleaned_time = line_splits[1].strip()

    if len(main_content_cleaned) <= 5:
        continue

    video_end_time = float(cleaned_time)

    if main_content_cleaned not in unique_lines:
        unique_lines.append(main_content_cleaned)
        unique_lines_with_info.append({'line': main_content_cleaned, 'time': cleaned_time})
        continue

    if main_content_cleaned not in valid_lines:
        valid_lines.append(main_content_cleaned)
        continue

valid_lines_with_info = [line_info for line_info in unique_lines_with_info if line_info['line'] in valid_lines]

for line_info in valid_lines_with_info:
    print(line_info)

print("video end time: ", video_end_time)

# clean_transcription_file = open('clean_transcription.txt', 'w')
# for valid_line in valid_lines:
#     print(valid_line, file=clean_transcription_file)
#
# clean_transcription_file.close()


