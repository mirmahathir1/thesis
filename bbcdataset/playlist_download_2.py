from pytube import Playlist
from os import listdir, mkdir
import os
from os.path import isfile, join
import time
import shutil
import string

def get_file_list_directory(directory_path, file_ext):
    file_list = [f for f in listdir(directory_path) if isfile(join(directory_path, f))]
    file_list = [a.split('.')[0] for a in file_list if file_ext in a]
    return file_list

# playlist = Playlist('https://www.youtube.com/playlist?list=PL5A4nPQbUF8Ck7csEOg98U0-bA970noXS')
playlist = Playlist('https://www.youtube.com/playlist?list=PLoijsUvO6bOX0kL94YYvrxvTOUxXzTkZw')

print('Number of videos in playlist online: %s' % len(playlist.video_urls))

raw_video_path = 'raw_videos'
raw_video_list = get_file_list_directory(raw_video_path, ".mp4")

def is_video_downloaded(url_title):
    return isfile(raw_video_path + "/" + url_title + ".mp4") \
        or isfile(raw_video_path + "/ignore/" + url_title + ".mp4") \
        or isfile(raw_video_path + "/selected/" + url_title + ".mp4")

for video in playlist.videos:
    start_time = time.time()
    url = video.watch_url

    title = video.title

    print('title: {}'.format(title))
    print('url: {}'.format(url))

    new_title = url.split("=")[1]

    if is_video_downloaded(new_title):
        print(f"skipping")
        continue

    shutil.rmtree(raw_video_path + "/temp")
    mkdir(raw_video_path + "/temp")

    try:
        video_stream = video.streams. \
            filter(type='video', progressive=True, file_extension='mp4'). \
            order_by('resolution'). \
            desc(). \
            first()
        video_stream.download(raw_video_path + "/temp")
    except Exception:
        print("error in downloading " + video.title + ". skipping...")
        continue

    downloaded_video = [f for f in listdir(raw_video_path + "/temp") if isfile(join(raw_video_path + "/temp", f))][0]

    current_file_path = "./" + raw_video_path + "/temp/" + downloaded_video
    destination_file_path = "./" + raw_video_path + "/" + new_title + ".mp4"

    os.rename(current_file_path, destination_file_path)

    print("--- %s seconds ---" % (time.time() - start_time))
