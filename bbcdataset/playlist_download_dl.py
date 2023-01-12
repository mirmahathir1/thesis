# include library
from pytube import Playlist, YouTube
import os
# CONTROLLER VARIABLES
# playlist_link = 'https://www.youtube.com/playlist?list=PL5A4nPQbUF8Ck7csEOg98U0-bA970noXS'
playlist_link = "https://www.youtube.com/playlist?list=PLoijsUvO6bOX0kL94YYvrxvTOUxXzTkZw"
playlist = Playlist(playlist_link)

number_of_videos_to_be_downloaded = len(playlist.video_urls)
# number_of_videos_to_be_downloaded = 50
path_to_raw_video_download = "./raw_videos"
# enable_download = False
enable_download = True

# CODE EXECUTION START
print("Total number of videos in playlist: ", len(playlist.video_urls))
# total_length_audio_in_bytes = 0
print("_" * 40)


def write_completed_url(new_url):
    logfile = open('completed_urls.txt', 'r')
    loglist = logfile.readlines()
    logfile.close()
    found = False
    for line in loglist:
        if new_url in line:
            print("Video Found")
            found = True
    if not found:
        logfile = open('completed_urls.txt', 'a')
        logfile.write(new_url + "\n")
        logfile.close()


def check_is_downloaded(url):
    logfile = open('completed_urls.txt', 'r')
    loglist = logfile.readlines()
    logfile.close()
    found = False
    for line in loglist:
        if url in line:
            found = True
    return found


for video_url in playlist.video_urls[:number_of_videos_to_be_downloaded]:
    print("_" * 40)

    print("Processing url: ", video_url)

    if check_is_downloaded(video_url):
        print("skipping download")
        continue

    if enable_download:
        print("Download: video start ")
        os.system('.\\youtube-dl.exe -f \'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4\' -o "./raw_videos/%(title)s.%(ext)s" '+video_url)
        print("Download: video end ")
        write_completed_url(video_url)

