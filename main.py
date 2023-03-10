import cv2 as cv
import numpy as np
import easyocr
from solver import *

# defining image dimensions
width = 900
height = 900

############ FUNCTIONS ############

# function that finds the biggest contour in the image:
# used to extract only the sudoku board
def detect_biggest_contour(contours):
    max_area, biggest = 0, np.array([])
    for i in contours:
        # Calculate the area of each contour, ignoring very low area ones
        area = cv.contourArea(i)
        if area <= 50: continue
        # Find the corners of each contour
        perimeter = cv.arcLength(i, True)
        corners = cv.approxPolyDP(i, 0.02 * perimeter, True)
        # Update the biggest contour and area 
        if area > max_area and len(corners) == 4:
            biggest, max_area = corners, area
    return biggest, max_area

# function that reorders contour points in the following order:
# top-left, top-right, bottom-left, bottom-right
def reorder_points(points):
    points = points.reshape((4, 2))
    ordered_points = np.zeros((4, 1, 2), dtype=np.int32)
    x_sum = points.sum(axis=1)
    ordered_points[0] = points[np.argmin(x_sum)]
    ordered_points[3] = points[np.argmax(x_sum)]
    y_diff = np.diff(points, axis=1)
    ordered_points[1] = points[np.argmin(y_diff)]
    ordered_points[2] = points[np.argmax(y_diff)]
    return ordered_points

# function that splits the sudoku board image into 81 small sudoku squares
def detect_small_squares(image):
    squares = [np.hsplit(row, 9) for row in np.vsplit(image, 9)]
    return [square for row in squares for square in row]

# function that detects numbers in the sudoku small squares:
# if no number is detected, 0 is saved (0 is not a valid sudoku number)
def detect_numbers(squares):
    reader = easyocr.Reader(['en'])
    detected_numbers = []
    new_detected_numbers = []
    for i in squares:
        # Read text from the square using OCR and allowing only numbers
        number = reader.readtext(i, allowlist="0123456789", mag_ratio=2)
        if not number:
            number = None
        detected_numbers.append(number)
    for j in detected_numbers:
        if not j:
            new_detected_numbers.append('0')
        else:
            new_detected_numbers.extend([k[1] for k in j])
    return new_detected_numbers

# function that writes numbers in the sudoku board
def display_numbers(image, numbers):
    square_width = width // 9
    square_height = height // 9
    for i, val in enumerate(numbers):
        if val != '0':
            x = i % 9
            y = i // 9
            # Place the detected number in the center of the square
            cv.putText(image, val, (x*square_width+square_width//2-10, int((y+0.8)*square_height)), 
                       cv.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2, cv.LINE_AA) 
    return image

############ SCRIPT ############

# load, show and resize the original, unsolved, sudoku board image
original = cv.imread('sudoku2.jpg')
cv.imshow('Original', original)
original = cv.resize(original, (width, height))

# load, show and resize an empty sudoku board image
blank_sudoku = cv.imread('blank_sudoku.jpg')
cv.imshow('Empty', blank_sudoku)
blank_sudoku = cv.resize(blank_sudoku, (width, height))

# convert the original to grayscale, then show 
gray = cv.cvtColor(original, cv.COLOR_BGR2GRAY)
cv.imshow('Gray', gray)

# blur the original using a 3x3 kernel, then show
blurred = cv.blur(gray, (3,3))
cv.imshow('Blurred', blurred)

# threshold the blurred, grayscale original, then show  
binarized = cv.adaptiveThreshold(blurred, 255, 1, 1, 11, 2)
cv.imshow('Binarized', binarized)

# create two copies of the original
original_1 = original.copy()
original_2 = original.copy()

# find and draw all the contours in the binarized image
contours, hierarchy = cv.findContours(binarized, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
cv.drawContours(original_1, contours, -1, (0, 0, 255), 3)

# find the biggest contour (sudoku board contour) 
biggest, max_area = detect_biggest_contour(contours)

# if a bigger contour is found, reorder and draw its points on original_2 
if biggest.size != 0:
    biggest = reorder_points(biggest)
    cv.drawContours(original_2, biggest, -1, (0,255,0), 10)

    # convert the points to float32 datatype
    p1 = np.float32(biggest)
    p2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    
    # compute a perspective transform in order to extract the sudoku board
    # (the image is transformed such that any quadrilateral shape
    # present in the image can be transformed into a rectangular shape
    # using a mapping process between the points)
    matrix = cv.getPerspectiveTransform(p1, p2)
    cropped = cv.warpPerspective(original, matrix, (width, height))

    # convert and show the cropped image to grayscale
    cropped_gray = cv.cvtColor(cropped, cv.COLOR_BGR2GRAY)
cv.imshow('Cropped gray', cropped_gray)

# detect small squares and numbers 
squares = detect_small_squares(cropped_gray)
numbers_but_in_chars = detect_numbers(squares)

numbers = []
for i in numbers_but_in_chars:
    # convert the detected numbers from string to integer data type
    numbers.append((ord(i) - ord('0')))

# split the list of numbers into 9 sub-lists of 9 numbers each
# (sudoku board rows)
board = np.array_split(numbers, 9)

# solve the sudoku board
solve(board)

numbers = []
numbers_but_in_chars = []

# concatenate the sub-lists of numbers into one single list
numbers = np.concatenate(board)

for i in numbers:
    # convert the numbers back to string datatype
    numbers_but_in_chars.append(str(i))

# create and display the result
result = display_numbers(blank_sudoku, numbers_but_in_chars)
cv.imshow('Result', result)

cv.waitKey(0)
cv.destroyAllWindows()
