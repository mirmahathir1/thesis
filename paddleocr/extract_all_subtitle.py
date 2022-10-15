import os
import cv2
import sys
from paddleocr import PaddleOCR
from os.path import exists
import numpy as np

ocr = PaddleOCR(use_angle_cls=True,
                lang='en', show_log = False)  # need to run only once to download and load model into memory

video_resolutions = dict()
for path, subdirs, files in os.walk('videos/white_background'):
    for name in files:
        file_path = os.path.join(path, name)  # change to your own video path
        print(file_path)
        if "ignore" in file_path:
            continue

        if exists(file_path.split('.')[0] + '.txt'):
            print(f"skipping {file_path}")
            continue

        print(f"video name: {file_path}")

        vid = cv2.VideoCapture(file_path)
        height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        print(f"resolution: {width}x{height}")

        frame_rate = int(vid.get(cv2.CAP_PROP_FPS))
        print(f"frame rate: {frame_rate}")

        frameCount = 0

        # Read until video is completed
        list_of_frames = []
        print("reading frames...")
        while vid.isOpened():
            # Capture frame-by-frame
            ret, frame = vid.read()
            if ret:
                if frameCount % frame_rate == 0:
                    list_of_frames.append(frame)
                    sys.stdout.write('.')  # same as print
                frameCount = frameCount + 1
            else:
                break
        print('')
        print(f"total count of frames:{len(list_of_frames)}")

        vid.release()
        print("applying ocr...")
        extracted_text = ""

        crop_height = 600
        crop_left = 0

        final_frame_count = len(list_of_frames)

        # check whether gdc foundation watermark is present in frame
        sample_frame = list_of_frames[final_frame_count // 2]
        sample_frame = sample_frame[600:,:,:]

        sample_frame = cv2.cvtColor(sample_frame, cv2.COLOR_BGR2GRAY)
        ret, sample_frame = cv2.threshold(sample_frame, 225, 255, cv2.THRESH_BINARY)


        result = ocr.ocr(sample_frame, cls=True)
        gdc_foundation_text = " ".join([line[1][0] for line in result]).lower()
        print(gdc_foundation_text)

        if 'foundation' in gdc_foundation_text:
            print("gdc foundation watermark found. moving crop left margin")
            crop_left = 300

        for index, frame in enumerate(list_of_frames):
            processed_frame = frame[crop_height:, crop_left:, :]

            ## simple thresholding
            # processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2GRAY)
            # ret, processed_frame = cv2.threshold(processed_frame, 10, 60, cv2.THRESH_BINARY)

            ## sayeed processing 2
            kernel = np.ones((5, 5), np.uint8)
            processed_frame = cv2.morphologyEx(processed_frame, cv2.MORPH_TOPHAT, kernel)

            ## sayeed thresholding
            # processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2GRAY)
            # ret, white = cv2.threshold(processed_frame, 225, 255, cv2.THRESH_BINARY)
            # ret, black = cv2.threshold(255 - processed_frame, 225, 255, cv2.THRESH_BINARY)
            # kernel = np.ones((9, 9), np.uint8)
            # closing = cv2.morphologyEx(black, cv2.MORPH_CLOSE,
            #                            kernel, iterations=1)
            # processed_frame = np.logical_not(np.logical_and(white > 127, closing > 127))
            # processed_frame = np.logical_not(processed_frame)
            # processed_frame = processed_frame.astype(np.uint8)  # convert to an unsigned byte
            # processed_frame *= 255

            # dilation_kernel = np.ones((2, 2), np.uint8)
            # processed_frame = cv2.dilate(processed_frame, dilation_kernel, iterations=1)

            cv2.imshow('Frame', processed_frame)
            cv2.waitKey(5)
            print('.', end='')
            result = ocr.ocr(processed_frame, cls=True)
            txts = [line[1][0] for line in result]
            print(f"detected texts: {' '.join(txts)}")
            extracted_text += (' '.join(txts) + "||" + str(index) + "%%") + '\n'
        textFile = open(file_path.split('.')[0] + '.txt', 'w')
        print(extracted_text, file=textFile)
        textFile.close()
