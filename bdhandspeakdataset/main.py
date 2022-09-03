import imutils

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import os
import cv2
import sys
from skimage.metrics import structural_similarity as compare_ssim

os.environ['TESSDATA_PREFIX'] = 'D:\\Documents\\ocr\\env\\share\\tessdata'

pytesseract.pytesseract.tesseract_cmd = r'D:\Documents\ocr\env\Library\bin\tesseract.exe'

cap = cv2.VideoCapture('sample.mp4')

frame_rate = 25

# Check if camera opened successfully
if not cap.isOpened():
    print("Error opening video stream or file")

textFile = open('transcription.txt', 'w')

frameCount = 0

# Read until video is completed
list_of_frames = []
while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret:
        if frameCount % frame_rate == 0:
            cropped_frame = frame[600:, :, :]
            # cropped_frame = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)
            # return_from_thresh, cropped_frame = cv2.threshold(cropped_frame, 200, 255, cv2.THRESH_BINARY)

            list_of_frames.append(cropped_frame)
            sys.stdout.write('.')  # same as print
        frameCount = frameCount + 1
    else:
        break

print('')

# When everything done, release the video capture object
cap.release()

print(len(list_of_frames))

for index, frame in enumerate(list_of_frames):
    cv2.imwrite(f"photos/{str(index).zfill(4)}.png",frame)
    # greyFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # return_from_thresh, threshFrame = cv2.threshold(greyFrame, 245, 255, cv2.THRESH_BINARY)
    # text_from_image = pytesseract.image_to_string(threshFrame)
    # cv2.imshow('Frame', frame)
    # cv2.waitKey(200)
    # print(text_from_image+"||"+str(frameCount / frame_rate)+"%%", file=textFile)

textFile.close()
