from pytube import Playlist

playlist = Playlist('https://www.youtube.com/playlist?list=PLAMGOR7JrXFJurRo0muFHv3BJ2kr4NrP4')
print('Number of videos in playlist: %s' % len(playlist.video_urls))

with open('videos\\download_complete.txt', encoding="utf-8") as f:
    download_completed_list = [line.strip() for line in f.readlines()]

print("completed videos: ")
print(download_completed_list)

completed_download_list_file = open('videos\\download_complete.txt', 'a', encoding="utf-8")
for video in playlist.videos:
    print('downloading : {} with url : {}'.format(video.title, video.watch_url))
    if video.title in download_completed_list:
        print("video already downloaded: "+video.title+". skipping...")
        continue
    try:
        video.streams.\
            filter(type='video', progressive=True, file_extension='mp4').\
            order_by('resolution').\
            desc().\
            first().\
            download('D:\\Documents\\ocr\\videos\\headlinenews')
        print(video.title, file=completed_download_list_file)
    except Exception:
        print("error in downloading "+video.title+". skipping...")
        continue
completed_download_list_file.close()
