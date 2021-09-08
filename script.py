import cv2
import datetime
import os
import tkinter
from tkinter import filedialog  # It only works like this????



# ----------
filename = "output.mp4"
filepath = ""
framerate = 30.0

timer_hours = 0
timer_minutes = 10
timer_seconds = 0

ol_font = cv2.FONT_HERSHEY_SIMPLEX
ol_font_size = 2
ol_line_width = 6
ol_color = (0,0,255) # color in BGR
ol_org = (50,100) # coordinates from top left
#------------


# ----- FILE SETUP
# FILENAME: yy_mm_dd_hh_mm
actual_start_time = datetime.datetime.now()
ast = actual_start_time
filename = "{}_{}_{}_{}_{}.mp4".format(ast.year,ast.month,ast.day,ast.hour,ast.minute)
# FILEPATH
tk = tkinter.Tk()
tk.withdraw()
currdir = os.getcwd()
filepath = filedialog.askdirectory(parent=tk, initialdir = currdir, title = 'Select File Save Location')
filename = os.path.join(filepath,filename)

# --- VIDEO SETUP
cap = cv2.VideoCapture(0) # Capture video from device default camera [0]

# Get the width and height of frame
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
framerate = cap.get(cv2.CAP_PROP_FPS)

# figure out how long to display each frame based off of fps
frameTime = int(1000/framerate)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(filename, fourcc, framerate, (width, height))




# ------ SCRIPT
# first, give tech a chance to set up the camera
print('Initializing Setup...')
while True:
    ret, frame = cap.read()
    if ret:
        cv2.putText(frame, 'Position Camera - Press "s" to start recording',ol_org,ol_font,ol_font_size,ol_color,ol_line_width)
        cv2.imshow('Place camera in proper position (pls make it straight)',frame)
        if (cv2.waitKey(1) & 0xFF) == ord('s'): # Hit 's' to start recording
            break
    else:
        break

# then, capture only this part of the video
# get start time
startTime = datetime.datetime.now()
difference_minutes = 0
print('Starting Recording...')
while(cap.isOpened() and (difference_minutes < timer_minutes)):
    ret, frame = cap.read()
    if ret:
        # write the frame
        out.write(frame)
        show_frame = frame  # frame to write on -> won't save to final video

        # refresh timer
        # get current time
        currentTime = datetime.datetime.now()
        # get time since start
        difference = currentTime - startTime

        # display frame
        cv2.putText(show_frame, str(difference)+" Press 'q' to exit",ol_org,ol_font,ol_font_size,ol_color,ol_line_width)
        cv2.imshow('RECORDING',frame)
        if ((cv2.waitKey(1) & 0xFF) == ord('q')): # Hit `q` to exit
            print('User break')
            break
        difference_minutes = currentTime.minute - startTime.minute
    else:
        break
print('Recording finished.')
# Release everything if job is finished
out.release()
cap.release()
cv2.destroyAllWindows()
