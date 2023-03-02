import cv2

img = cv2.imread('images/input.jpg')

filtered = cv2.GaussianBlur(img, (5, 5), 1.5)

cv2.imshow('Original image', img)
cv2.waitKey(0)

cv2.imshow('Gaussian filtered image', filtered)
cv2.waitKey(0)

cv2.destroyAllWindows()
