import cv2
import numpy as np
import pandas as pd

video_name = '50 Lac poor people were receiving the cash assistance from BD government.mp4'
cap = cv2.VideoCapture(f"../extractedbdhandspeakskeletons/reduced_framerate_raw_videos/{video_name}")

dataframe = pd.read_csv(f"csv_files/{video_name.split('.')[0]}.csv")
print(dataframe.columns)

if (cap.isOpened()== False): 
  print("Error opening video stream or file")

frame_count = 0
while(cap.isOpened()):
  ret, frame = cap.read()
  if ret == True:
    # print(dataframe.iloc[frame_count])
    for i in range(137):
        x = int(dataframe.iloc[frame_count,1+i*2])
        y = int(dataframe.iloc[frame_count,1+i*2+1])
        cv2.circle(frame,(x, y), 5, (255,0,0), -1)
    cv2.imshow('Frame',frame)
    
    frame_count += 1
 
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break

  else: 
    break

cap.release()
 
cv2.destroyAllWindows()