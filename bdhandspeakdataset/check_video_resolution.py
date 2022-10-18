import os
import cv2

video_resolutions = dict()
for path, subdirs, files in os.walk('videos'):
    for name in files:
        file_path = os.path.join(path, name)  # change to your own video path
        print(file_path)
        if "ignore" in file_path:
            continue

        vid = cv2.VideoCapture(file_path)
        height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        # print(f"{height}x{width}")
        if f"{height}x{width}" in video_resolutions:
            video_resolutions[f"{height}x{width}"] += 1
        else:
            video_resolutions[f"{height}x{width}"] = 1
        vid.release()

print(video_resolutions)
