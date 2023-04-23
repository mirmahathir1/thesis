import shutil
import os
from os import listdir
from os.path import isfile, join
import subprocess
import time
import sys
sys.path.append('../')
import lib

os.chdir('openpose')

path_to_videos = '..\\..\\presentation\\selected\\'
drive_log_directory = '..\\extracted_skeletons\\'


def is_already_extracted(video_file_base):
    return os.path.isfile(f"{drive_log_directory}/{video_file_base}.zip")


video_list = lib.get_file_list_directory(path_to_videos, '.avi')
# video_list = ["n2LPq88ZQyM_cropped_reduced"]
incomplete_videos = [video for video in video_list if not is_already_extracted(video)]

# print("total videos: ")
# print(video_list)
print(f"total video count: {len(video_list)}")


# print("incomplete videos")
# print(incomplete_videos)
print(f"incomplete video count: {len(incomplete_videos)}")

for video in incomplete_videos:
    start_time = time.time()
    video_file_base = video
    if is_already_extracted(drive_log_directory + video_file_base + '.avi'):
        print("skipping " + video_file_base)
        continue

    if os.path.exists('..\\active_output.avi'):
        os.remove('..\\active_output.avi')

    if os.path.exists('..\\active.avi'):
        os.remove('..\\active.avi')

    shutil.rmtree('..\\tmp_jsons', ignore_errors=True)
    os.makedirs('..\\tmp_jsons', exist_ok=True)

    print("name of video: " + video_file_base)

    shutil.copy(path_to_videos + video_file_base+'.avi', '..\\active.avi')

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
    shutil.make_archive('..\\' + video_file_base, 'zip',
                        '..\\tmp_jsons\\')
    print("moving to drive...")
    shutil.move('..\\' + video_file_base + '.zip',
                drive_log_directory + video_file_base + '.zip')
    shutil.move("..\\active_output.avi", "..\\videos_with_skeletons\\"+video_file_base+".avi")
    print(f"---- time: {(time.time() - start_time) / 60} minutes-----")
