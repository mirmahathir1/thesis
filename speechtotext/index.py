import lib
import pandas as pd
from google.cloud import speech
# https://cloud.google.com/speech-to-text/docs/quickstart
# gsutil cp -r extracted_audio_segments gs://speechdata123/
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "F:\\thesis\\speechtotext\\config\\hybrid-task-381815-4e81bcf46e16.json"

# Instantiates a client
client = speech.SpeechClient()

file_list = lib.get_file_list_directory_recurse("../extractedbtvdataset/extracted_audio_segments",".mp3")

transcript_root_folder = "text_transcripts"

for file_path in file_list:
    [root, folder, audio_name] = file_path.split("\\")
    gcs_uri = f"gs://speechdata123/extracted_audio_segments/{folder}/{audio_name}"
    print(gcs_uri)
    lib.makedir(f"{transcript_root_folder}/{folder}")

    transcript_dataframe = pd.DataFrame(columns=['word','start_time','end_time'])
    transcript_csv_file = audio_name.replace(".mp3",".csv")

    if lib.isfile(f"{transcript_root_folder}/{folder}/{transcript_csv_file}"):
        print("skip")
        continue

    audio = speech.RecognitionAudio(uri=gcs_uri)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
        sample_rate_hertz=16000,
        language_code="bn-BD",
        enable_word_time_offsets=True,
        enable_automatic_punctuation=True,
    )

    # Detects speech in the audio file
    operation = client.long_running_recognize(config=config, audio=audio)
    response = operation.result(timeout=90)

    text_line_root = "text_lines"
    lib.makedir(f"{text_line_root}/{folder}")
    text_file_name = audio_name.replace(".mp3",".txt")
    text_line_file = open(f"{text_line_root}/{folder}/{text_file_name}","w",encoding='utf-8')

    for result in response.results:
        alternative = result.alternatives[0]
        print("Transcript: {}".format(alternative.transcript))
        print("Confidence: {}".format(alternative.confidence))
        print(f"{alternative.transcript}", file=text_line_file)

        for word_info in alternative.words:
            word = word_info.word
            start_time = word_info.start_time
            end_time = word_info.end_time

            new_row = pd.DataFrame({
                'word': word, 
                'start_time': start_time.total_seconds(), 
                'end_time': end_time.total_seconds()}, index=[0])
            transcript_dataframe = pd.concat([transcript_dataframe.loc[:],new_row]).reset_index(drop=True)
        break

    text_line_file.close()
    transcript_dataframe.to_csv(f"{transcript_root_folder}/{folder}/{transcript_csv_file}", encoding='utf-8')
