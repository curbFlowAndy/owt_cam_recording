import cv2
import datetime
import os
import platform
import tkinter
from tkinter import filedialog  # It only works like this????



# ----------
filename = "output.mp4"
filepath = ""
os_xt = "mp4"

framerate = 30.0
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

timer_hours = 0
timer_minutes = 10
timer_seconds = 0

ol_font = cv2.FONT_HERSHEY_SIMPLEX
ol_font_size = 2
ol_line_width = 6
ol_color = (0,0,255) # color in BGR
ol_org = (50,100) # coordinates from top left
#------------


# ------ OS DETECTION
plt = platform.system()
if plt == "Windows":
    print("\nWINDOWS IS UNSUPPORTED\n")
elif plt == "Linux":
    print("\nLinux Detected\n")
    os_xt = ".h264"
    fourcc = cv2.VideoWriter_fourcc(*'H264')
elif plt == "Darwin":
    print("\nMacOS Detected\n")
    # no need for additional config because defaults reflect macOS


# ----- FILE SETUP
# FILENAME: yy.mm.dd_hh.mm
actual_start_time = datetime.datetime.now()
ast = actual_start_time
filename = "{}.{}.{}_{}.{}.{}".format(ast.year,ast.month,ast.day,ast.hour,ast.minute,os_xt)
# FILEPATH
tk = tkinter.Tk()
tk.withdraw()
currdir = os.getcwd()
filepath = filedialog.asksaveasfilename(parent = tk, defaultextension = '.mp4', initialfile = filename, title = "Choose Save Location")

# --- VIDEO SETUP
cap = cv2.VideoCapture(0) # Capture video from device default camera [0]
cap2 = cv2.VideoCapture(1)


# Get the width and height of frame
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
# framerate = cap.get(cv2.CAP_PROP_FPS)

# figure out how long to display each frame based off of fps
frameTime = int(1000/framerate)

# Define the codec and create VideoWriter object
out = cv2.VideoWriter(filepath, fourcc, framerate, (width, height))





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
        print(str(difference)+'\nPress "q" to stop recording')
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
