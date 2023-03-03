import cv2

img = cv2.imread('images/input.jpg', cv2.IMREAD_COLOR)
# img = cv2.imread('images/input.jpg', cv2.IMREAD_GRAYSCALE)
# img = cv2.imread('images/input.jpg', cv2.IMREAD_UNCHANGED)

# resize the image according to specified width and height 
# img = cv2.resize(img, (400, 400)) 

# halves image size
img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5) 

# rotates the image
# img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

# creates a new image file
cv2.imwrite('images/output.jpg', img)

cv2.imshow('Bear', img)

# cv2.waitKey(5) waits 5 seconds to any key to be pressed
cv2.waitKey(0)  # waits to any key to be pressed
cv2.destroyAllWindows()