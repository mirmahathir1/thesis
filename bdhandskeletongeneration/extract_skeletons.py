import shutil
import os
from os import listdir
from os.path import isfile, join
import subprocess
import time

os.chdir('openpose')

path_to_videos = '..\\reduced_videos\\'
drive_log_directory = '..\\extracted_skeletons\\'


def is_already_extracted(video_file_base):
    return os.path.isfile(drive_log_directory + video_file_base + '.zip')


video_list = [f for f in listdir(path_to_videos) if isfile(join(path_to_videos, f))]

video_list.sort(reverse=True)

for video in video_list:
    start_time = time.time()
    video_file_base = video.split('.')[0]
    if is_already_extracted(video_file_base):
        print("skipping " + video_file_base)
        continue

    if os.path.exists('..\\active_output.avi'):
        os.remove('..\\active_output.avi')

    if os.path.exists('..\\active.avi'):
        os.remove('..\\active.avi')

    shutil.rmtree('..\\tmp_jsons', ignore_errors=True)
    os.makedirs('..\\tmp_jsons', exist_ok=True)

    print("name of video: " + video_file_base)
    print("started extraction of avi file...")

    result = subprocess.run(['ffmpeg', '-i', '..\\reduced_videos\\'+video_file_base+'.mp4', '-c:a', 'aac', '-c:v', 'libx264', '-b:a', '384K', '..\\active.avi'])
    # ffmpeg -i input.mp4 -c:v libx264 -c:a libmp3lame -b:a 384K output.avi
    print("stdout:", result.stdout)
    print("stderr:", result.stderr)
    if result.stderr:
        print("fatal error in converting to avi")
        exit(1)

    shutil.copy('..\\active.avi', '..\\avi_files\\'+video_file_base+'.avi')

    print("extracting skeletons...")

    result = subprocess.run(
        ['.\\bin\\OpenPoseDemo.exe', "--video", "..\\active.avi", "--write_json",
         '..\\tmp_jsons', "--display", "0", "--write_video",
         "..\\" + 'active_output.avi', "--face", "--hand"],
        capture_output=True, text=True)
    print("stdout:", result.stdout)
    print("stderr:", result.stderr)
    if not len(result.stderr) == 0:
        print("fatal error in openpose extraction")
        exit(1)
    print("zipping logs...")
    shutil.make_archive('..\\' + video_file_base.strip(), 'zip',
                        '..\\tmp_jsons\\')
    print("moving to drive...")
    shutil.move('..\\' + video_file_base.strip() + '.zip',
                '..\\extracted_skeletons\\' + video_file_base.strip() + '.zip')
    shutil.move("..\\active_output.avi", "..\\videos_with_skeletons\\"+video_file_base+".avi")
    print(f"---- time: {(time.time() - start_time) / 60} minutes-----")
