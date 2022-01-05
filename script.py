import cv2
import numpy as np
import datetime
import os
import platform
import tkinter
from tkinter import filedialog
from math import floor



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
caps = []   # hold all captures
outs = []   # for the output streams
for i in range(0,3):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        while True:
            ret,frame = cap.read()
            if ret:
                cv2.putText(frame,"'y' to keep, 'n' to ignore",ol_org,ol_font,ol_font_size,ol_color,ol_line_width)
                cv2.imshow('Frame',frame)
                key = (cv2.waitKey(1) & 0xFF)
                if key == ord('y'):
                    caps.append(cap)

                    # get frame data
                    width = int(caps[0].get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
                    height = int(caps[0].get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
                    framerate = cap.get(cv2.CAP_PROP_FPS)

                    # fix file name
                    filepath = filepath.split('.mp4')
                    filepath = filepath[0]  # everything before the .mp4
                    filepath = filepath + '_' + str(i) + '.mp4'

                    print('Filepath added:\t'+filepath)
                    outs.append(cv2.VideoWriter(filepath,fourcc,framerate,(width,height)))
                    break

                elif key == ord('n'):
                    break
            else:
                break


# capture the footage
#cv2.destroyAllWindows()
start_time = datetime.datetime.now()
difference_minutes = 0
print('Starting Recording...')
while True:
    # get current time and increment timer
    current_time = datetime.datetime.now()
    time_passed = current_time - start_time
    time_passed_minutes = floor(time_passed.seconds / 60)
    if time_passed_minutes >= 10:
        print('Time limit reached.')
        break
    time_passed_string = "{}:{}:{}".format(time_passed_minutes,(time_passed.seconds % 60),time_passed.microseconds)

    # write output files for current frame on each stream
    frames = []
    for cap in caps:
        ret,frame = cap.read()
        if ret:
            frames.append(frame)
            outs[caps.index(cap)].write(frame)

    # display frames
    if len(frames) > 1:
        frames = np.concatenate((frames[0],frames[1]),axis=0)
    else:
        frames = frames[0]

    cv2.putText(frames,"{} Press 'q' to quit".format(time_passed_string),ol_org,ol_font,ol_font_size,ol_color,ol_line_width)
    cv2.imshow("RECORDING",frames)
    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        print('Stream canceled by user.')
        break

print('Recording finished.')
# Release everything if job is finished
for i in range(0,len(outs)):
    caps[i].release()
    outs[i].release()
cv2.destroyAllWindows()
