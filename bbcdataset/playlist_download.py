from pytube import Playlist
from os import listdir
from os.path import isfile, join
import string
import time

playlist = Playlist('https://www.youtube.com/playlist?list=PL5A4nPQbUF8Ck7csEOg98U0-bA970noXS')
print('Number of videos in playlist online: %s' % len(playlist.video_urls))

cropped_video_path = 'cropped_reduced_videos'
existing_cropped_videos = [f for f in listdir(cropped_video_path) if isfile(join(cropped_video_path, f))]
existing_cropped_videos = [a.split('.')[0] for a in existing_cropped_videos if '.mp4' in a]

print(f"Existing cropped video: ")
for existing_cropped_video in existing_cropped_videos:
    print(existing_cropped_video)

print('Number of cropped videos in playlist online: %s' % len(existing_cropped_videos))

existing_raw_video_file = open('raw_video_completed.txt', encoding='utf-8')
existing_raw_videos = [line.strip() for line in existing_raw_video_file.readlines()]
existing_raw_video_file.close()


def simplify_video_name(name):
    return_string = "".join(name.translate(str.maketrans('', '', string.punctuation)).split()).lower()
    return return_string


print("Existing Raw Videos:")
for raw_video_name in existing_raw_videos:
    print(raw_video_name)

print('Number of raw videos in playlist offline: %s' % len(existing_raw_videos))

completed_download_list_file = existing_raw_videos + existing_cropped_videos

completed_download_list_file = [simplify_video_name(file_name) for file_name in completed_download_list_file]

print(f"Total raw and cropped videos: {len(completed_download_list_file)}")

ignore_url_file = open('ignore_list.txt')
ignore_url_list = [line.strip() for line in ignore_url_file.readlines()]
ignore_url_file.close()

skipped_online_video_count = 0
for video in playlist.videos:
    start_time = time.time()
    url = video.watch_url

    if url in ignore_url_list:
        print("skipping url {} because it exists in ignored urls".format(url))
        continue

    title = video.title
    print('title: {}'.format(title))
    print('url: {}'.format(url))

    if simplify_video_name(title) in completed_download_list_file:
        print("video already downloaded as raw/cropped: " + title + ". skipping...")
        skipped_online_video_count = skipped_online_video_count + 1
        continue
    try:
        video.streams. \
            filter(type='video', progressive=True, file_extension='mp4'). \
            order_by('resolution'). \
            desc(). \
            first(). \
            download('raw_videos')
        existing_raw_video_file = open('raw_video_completed.txt', 'a', encoding='utf-8')
        print(title, file=existing_raw_video_file)
        existing_raw_video_file.close()
    except Exception:
        print("error in downloading " + video.title + ". skipping...")
        continue
    print("--- %s seconds ---" % (time.time() - start_time))

print(f"skipped online video count: {skipped_online_video_count}")
