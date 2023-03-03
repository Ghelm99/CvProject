import cv2
import numpy as np

# accessing the webcam
capture = cv2.VideoCapture(0)

while True:
    ret, frame = capture.read() # ret tells if the capture is ok
    width = int(capture.get(3)) # 3 represents the capture property width
    height = int(capture.get(4))

    # define an HSV image
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([130, 255, 255])
 
    # tells which pixels are between the two blues
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # bitwise images with an algebra operation
    result = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow('Webcam', result)
    if cv2.waitKey(1) == ord('q'):  # terminate video if pressing q
        break

capture.release() # releases the camera resource to other programs
cv2.destroyAllWindows() 