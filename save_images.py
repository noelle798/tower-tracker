import numpy as np
import cv2

# name images [height difference between bottom of tape U and camera height] - [horizontal distance from camera to tape]

cap = cv2.VideoCapture(2)

while(cv2.waitKey(1) & 0xFF != ord('q')):
    ret, image = cap.read()
    cv2.imshow('image', image)

    if(cv2.waitKey(1) & 0xFF == ord(' ')):
        name = raw_input("name: ")
        cv2.imwrite(name + ".jpg", image)

cap.release()
cv2.destroyAllWindows()
