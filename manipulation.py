import cv2
import random

img = cv2.imread('images/input.jpg', cv2.IMREAD_COLOR)

# print(img) -> when reading an image I create a numpy array
# print(type(img)) -> numpy array

# prints the image dimensions (as a 3D numpy array)
print(img.shape) 

# in opencv the order is BGR, not RGB.
print(img[0][45:400]) # pixels from 45 to 400, first row

# adding random colors to an image
for i in range(100):
    for j in range(img.shape[1]):
        img[i][j] = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]

# copy a part of the image to somewhere else
tag = img[300:400, 100:200] 
img[100:200, 650:750] = tag


cv2.imshow('Bear', img)
cv2.waitKey(0)
cv2.destroyAllWindows()