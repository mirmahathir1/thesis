from matplotlib.widgets import RectangleSelector
import matplotlib.pyplot as plt
import lib
from moviepy.editor import *

import random

# plt.rcParams["figure.figsize"] = [14, 7]
# plt.rcParams["figure.autolayout"] = True


video_file_root = 'raw_videos/selected'
all_video_files = lib.get_file_list_directory(video_file_root,'mp4')

for video_file in all_video_files:
    video_file_name = f"{video_file_root}/{video_file}.mp4"
    text_file_name = f"raw_videos/selected_coordinates/{video_file}_coordinates.txt"
    print(video_file_name)

    if lib.isfile(text_file_name):
        print(f"coordinates already extracted")
        continue

    clip = VideoFileClip(video_file_name)

    confirmed_coordinates = None

    while True:
        def onselect_function(eclick, erelease):
            global confirmed_coordinates
            # Obtain (xmin, xmax, ymin, ymax) values
            # for rectangle selector box using extent attribute.
            extent = rect_selector.extents
            confirmed_coordinates = extent
            print("Extents: ", extent)
        
        # plot a line graph for data n
        fig, ax = plt.subplots()
        frame = clip.get_frame(random.randrange(int(clip.duration)))
        im = ax.imshow(frame)
        
        # Define a RectangleSelector at given axes ax.
        # It calls a function named 'onselect_function'
        # when the selection is completed.
        # Rectangular box is draw s allowed for doing selection.
        rect_selector = RectangleSelector(
            ax, onselect_function, drawtype='box', button=[1])
        
        # Display graph
        mng = plt.get_current_fig_manager()
        mng.window.showMaximized()
        plt.show()

        if not confirmed_coordinates == None and input(f"is the cropping ok? (y/n)")=='y':
            break
    
    output_file = open(text_file_name,"w")
    print(confirmed_coordinates, file=output_file)
    output_file.close()
