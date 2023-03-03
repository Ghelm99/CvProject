import cv2
import numpy as np

# accessing the webcam
capture = cv2.VideoCapture(0)

while True:
    ret, frame = capture.read() # ret tells if the capture is ok
    width = int(capture.get(3)) # 3 represents the capture property width
    height = int(capture.get(4))

    # drawing a line, the origin of the axis correspond to the top left corner
    img = cv2.line(frame, (0, 0), (width, height), (255, 0, 0), 10)
    img = cv2.line(img, (0, height), (width, 0), (0, 255, 0), 5)

    # drawing a rectangle
    img = cv2.rectangle(img, (100, 100), (200, 200), (128, 128, 128), 5)

    # drawing a circle
    img = cv2.circle(img, (300, 300), 60, (0, 0, 255), -1)

    # drawing text
    font = cv2.FONT_HERSHEY_SIMPLEX
    img = cv2.putText(img, 'Galmu', (200, height - 10), font, 4, (150, 0, 0), 5, cv2.LINE_AA)
    
    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) == ord('q'):  # terminate video if pressing q
        break

capture.release() # releases the camera resource to other programs
cv2.destroyAllWindows() 