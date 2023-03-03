import cv2
import numpy as np

# accessing the webcam
capture = cv2.VideoCapture(0)

while True:
    ret, frame = capture.read() # ret tells if the capture is ok
    width = int(capture.get(3)) # 3 represents the capture property width
    height = int(capture.get(4))

    image = np.zeros(frame.shape, np.uint8) # black frame
    smaller_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    image[:height//2, :width//2] = cv2.rotate(smaller_frame, cv2.ROTATE_180)
    image[height//2:, :width//2] = smaller_frame
    image[:height//2, width//2:] = smaller_frame
    image[height//2:, width//2:] = smaller_frame

    cv2.imshow('Webcam', image)
    if cv2.waitKey(1) == ord('q'):  # terminate video if pressing q
        break

capture.release() # releases the camera resource to other programs
cv2.destroyAllWindows() 