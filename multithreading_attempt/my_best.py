from __future__ import print_function
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import argparse
import imutils
import cv2

vs = WebcamVideoStream(src=1).start()
fps = FPS().start()

while True:
    frame = vs.read()
    frame = imutils.resize(frame, width = 400)

    cv2.imshow("Frame",frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

    fps.update()

fps.stop()
cv2.destroyAllWindows()
vs.stop()
