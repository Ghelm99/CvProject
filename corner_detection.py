import numpy as np
import cv2 

img = cv2.imread('images/chessboard.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# corners detection
corners = cv2.goodFeaturesToTrack(gray, 100, 0.01, 10)
corners = np.int0(corners)

for corner in corners:
    x, y = corner.ravel()
    cv2.circle(img, (x, y), 5, (255, 0, 0), -1)

cv2.imshow('Frame', img)

cv2.waitKey(0)
cv2.destroyAllWindows()