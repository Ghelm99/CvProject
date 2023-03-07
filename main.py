import cv2 as cv
import numpy as np
import imutils
import easyocr

original = cv.imread('images/car5.jpg')
# cv.imshow('Original', original)

gray = cv.cvtColor(original, cv.COLOR_BGR2GRAY)
# cv.imshow('Gray', gray)

filtered = cv.bilateralFilter(gray, 9, 75, 75)
 # cv.imshow('Filtered', filtered)

edged = cv.Canny(filtered, 30, 200)
# cv.imshow('Edged', edged)

new_edged = edged
keypoints = cv.findContours(new_edged, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(keypoints)
contours = sorted(contours, key=cv.contourArea, reverse=True)[:10]

location = None
for contour in contours:
    approx = cv.approxPolyDP(contour, 10, True)
    if len(approx) == 4:
        location = approx
        break
    
if location is not None:
    mask = np.zeros(gray.shape, np.uint8)
    plate = cv.drawContours(mask, [location], 0,255, -1)
    plate = cv.bitwise_and(original, original, mask=mask)
else:
    print("Failed to find plate location.")

(x,y) = np.where(mask==255)
(x1, y1) = (np.min(x), np.min(y))
(x2, y2) = (np.max(x), np.max(y))
cropped_image = gray[x1:x2+1, y1:y2+1]

cv.imshow('Cropped', cropped_image)

reader = easyocr.Reader(['en'])
result = reader.readtext(cropped_image)
print(result)

cv.waitKey(0)
cv.destroyAllWindows()