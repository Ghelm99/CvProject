import cv2 as cv
import numpy as np
import easyocr
from solver import *

width = 900
height = 900

def detect_biggest_contour(contours):
    max_area, biggest = 0, np.array([])
    
    for i in contours:
        area = cv.contourArea(i)
        if area <= 50: continue
        
        perimeter = cv.arcLength(i, True)
        corners = cv.approxPolyDP(i, 0.02 * perimeter, True)
        
        if area > max_area and len(corners) == 4:
            biggest, max_area = corners, area
    
    return biggest, max_area


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


def detect_small_squares(img):
    squares = [np.hsplit(row, 9) for row in np.vsplit(img, 9)]
    return [square for row in squares for square in row]


def detect_numbers(squares):
    reader = easyocr.Reader(['en'])
    numbers = []
    new_numbers = []
    for i in squares:
        number = reader.readtext(i, allowlist="0123456789", mag_ratio=2)
        if not number:
            number = None
        numbers.append(number)
    for j in numbers:
        if not j:
            new_numbers.append('0')
        else:
            new_numbers.extend([k[1] for k in j])
    return new_numbers


def display_numbers(blank, numbers):
    square_width = width // 9
    square_height = height // 9
    for i, val in enumerate(numbers):
        if val != '0':
            x = i % 9
            y = i // 9
            cv.putText(blank, val, (x*square_width+square_width//2-10, int((y+0.8)*square_height)), 
                       cv.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2, cv.LINE_AA) 
    return blank

# image pre-processing
original = cv.imread('sudoku2.jpg')
cv.imshow('Original', original)
original = cv.resize(original, (width, height))
blank_sudoku = cv.imread('blank_sudoku.jpg')
blank_sudoku = cv.resize(blank_sudoku, (width, height))
gray = cv.cvtColor(original, cv.COLOR_BGR2GRAY)
blurred = cv.blur(gray, (3,3))
thresholded = cv.adaptiveThreshold(blurred, 255, 1, 1, 11, 2)

# contours detection
original_contours = original.copy()
original_big_contours = original.copy()
contours, hierarchy = cv.findContours(thresholded, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
cv.drawContours(original_contours, contours, -1, (0, 255, 0), 3)
biggest, max_area = detect_biggest_contour(contours)
if biggest.size != 0:
    biggest = reorder_points(biggest)
    cv.drawContours(original_big_contours, biggest, -1, (0,255,0), 10)
    p1 = np.float32(biggest)
    p2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    matrix = cv.getPerspectiveTransform(p1, p2)
    cropped = cv.warpPerspective(original, matrix, (width, height))
    cropped_colored = cv.cvtColor(cropped, cv.COLOR_BGR2GRAY)

cv.imshow('Cropped colored', cropped_colored)

squares = detect_small_squares(cropped_colored)
numbers = detect_numbers(squares)

new_numbers = []
for i in numbers:
    new_numbers.append((ord(i) - ord('0')))

board = np.array_split(new_numbers, 9)
solve(board)

numbers = np.concatenate(board)

new_numbers = []
for i in numbers:
    new_numbers.append(str(i))

result = display_numbers(blank_sudoku, new_numbers)
cv.imshow('Result', result)

cv.waitKey(0)
cv.destroyAllWindows()
