crop_height = 600
crop_left = 0

final_frame_count = len(list_of_frames)

# check whether gdc foundation watermark is present in frame
sample_frame = list_of_frames[10]
sample_frame = sample_frame[600:,:,:]
sample_frame = cv2.cvtColor(sample_frame, cv2.COLOR_BGR2GRAY)
ret, white = cv2.threshold(sample_frame, 225, 255, cv2.THRESH_BINARY)
# gauss = cv2.adaptiveThreshold(sample_frame,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
# ret2,otsu = cv2.threshold(sample_frame,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
ret, black = cv2.threshold(255-sample_frame, 225, 255, cv2.THRESH_BINARY)

# figure(figsize=(12, 6), dpi=80)
# plt.imshow(cv2.cvtColor(255-white, cv2.COLOR_BGR2RGB))
# figure(figsize=(12, 6), dpi=80)
# plt.imshow(cv2.cvtColor(gauss, cv2.COLOR_BGR2RGB))
# figure(figsize=(12, 6), dpi=80)
# plt.imshow(cv2.cvtColor(otsu, cv2.COLOR_BGR2RGB))


# figure(figsize=(12, 6), dpi=80)
# plt.imshow(cv2.cvtColor(black, cv2.COLOR_BGR2RGB))


kernel = np.ones((9, 9), np.uint8)
# Using cv2.erode() method
# erode = cv2.dilate(black, kernel)

# figure(figsize=(12, 6), dpi=80)
# plt.imshow(cv2.cvtColor(erode, cv2.COLOR_BGR2RGB))

# processed_erode = np.logical_and(white>127, erode>127)
# figure(figsize=(12, 6), dpi=80)
# plt.imshow(processed_erode, cmap=plt.cm.gray)


closing = cv2.morphologyEx(black, cv2.MORPH_CLOSE,
                           kernel, iterations=1)
# figure(figsize=(12, 6), dpi=80)
# plt.imshow(closing, cmap=plt.cm.gray)

processed_closing = np.logical_not(np.logical_and(white>127, closing>127))
figure(figsize=(12, 6), dpi=80)
plt.imshow(processed_closing, cmap=plt.cm.gray)