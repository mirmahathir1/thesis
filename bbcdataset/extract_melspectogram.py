import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

from moviepy.editor import *

sound = AudioFileClip("../extractedbtvdataset/cropped_reduced_videos/_FW0SkPpsC8_cropped_reduced.mp4")
# sound = AudioFileClip("../extractedbtvdataset/cropped_reduced_videos/_u6jEqimZdc_cropped_reduced.mp4")
sound.write_audiofile("tmp/sound.wav", 44100, 2, 2000,"pcm_s32le")

filename = 'tmp/sound.wav'
n_fft = 2048
hop_length = 512
n_mels = 80

y, sr = librosa.load(filename)
print(f"duration: {librosa.get_duration(y=y, sr=sr)}")
# trim silent edges
whale_song, _ = librosa.effects.trim(y)
# librosa.display.waveplot(whale_song, sr=sr);
S = librosa.feature.melspectrogram(whale_song, sr=sr, n_fft=n_fft, hop_length=hop_length, n_mels=n_mels)
S_DB = librosa.power_to_db(S, ref=np.max)
print(S_DB)
print(S_DB.shape)

# duration
# 1609.1 seconds
# (80, 69295)
# division: 43.064

# duration
# 855.2 seconds
# (80, 36828)
# division: 43.063