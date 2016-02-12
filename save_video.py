import numpy as np
import cv2

camera = cv2.VideoCapture(2)

fps = 100, # camera.get(CV_CAP_PROP_FPS) # doesn't work for webcams
size = (640, 480) # (camera.get(CV_CAP_PROP_FRAME_WIDTH), camera.get(CV_CAP_PROP_FRAME_HEIGHT)) # doesn't work for webcams

video = cv2.VideoWriter("video2.avi", -1, -1, size)
print "fps:", fps
print "size:", size

while(cv2.waitKey(1) & 0xFF != ord('q')):
    _, image = camera.read()
    # cv2.imshow('image', image)
    video.write(image)

cv2.destroyAllWindows()
camera.release()
