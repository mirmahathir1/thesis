from paddleocr import PaddleOCR,draw_ocr
import cv2
# Paddleocr supports Chinese, English, French, German, Korean and Japanese.
# You can set the parameter `lang` as `ch`, `en`, `french`, `german`, `korean`, `japan`
# to switch the language model in order.
ocr = PaddleOCR(use_angle_cls=True, lang='en') # need to run only once to download and load model into memory
img_path = 'problem2.png'

image = cv2.imread(img_path)
processed_image = image
processed_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ret, processed_image = cv2.threshold(processed_image, 20, 50, cv2.THRESH_BINARY)
result = ocr.ocr(processed_image, cls=True)
for line in result:
    print(line)

cv2.imshow('sample', processed_image)
cv2.waitKey(0)