import cv2
import matplotlib.pyplot as plt
import numpy as np
import PIL

from utils import *


def get_contractions_ranges(img, show_image:bool=False):
    green_segmented_img = Segmentation.segment_green(img)
    
    contours, _ = Contours.get_contours(green_segmented_img)
    max_contour = max(contours, key=lambda cnt: cv2.boundingRect(cnt)[1])
    
    _, y, _, h = cv2.boundingRect(max_contour)
    
    # Find all pixels with y-coordinate greater than or equal to max_contour's y-coordinate
    selected_points = [[i, j] for point in max_contour for i, j in [point[0]] if j >= y + h - 1]

            
    if len(selected_points)%2 != 0:
        print("ERROR: Getting contractions range!!!!!")
    
    ranges = [int((p1[0] + p2[0]) / 2) for p1, p2 in zip(selected_points[::2], selected_points[1::2])]
    
    if show_image:
        Prints.print_img_per_x_and_show(green_segmented_img, ranges)
    
    return ranges
    

def get_contour_y_range(contour):
    # Find the bounding rectangle of the contour
    x, y, w, h = cv2.boundingRect(contour)

    # Calculate the maximum and minimum y-coordinates
    max_y = y + h
    min_y = y

    return min_y, max_y


def get_contour_with_largest_height(contours):
    # Initialize variables to store information about the contour with the largest height
    max_height = 0
    contour_with_max_height = None

    # Iterate through all contours
    for contour in contours:
        # Get the bounding rectangle of the contour
        x, y, w, h = cv2.boundingRect(contour)

        # Check if the current contour has a larger height than the previous maximum
        if h > max_height:
            max_height = h
            contour_with_max_height = contour

    return contour_with_max_height


def get_contractions_per_range(img, min_x, max_x, show_image:bool=False):
    
    black_segmented_img = Segmentation.detect_and_paint(img)
    segmented_img = black_segmented_img[:, min_x:max_x]
    
    gray = cv2.cvtColor(segmented_img, cv2.COLOR_BGR2GRAY)

    # Apply binary thresholding
    _, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

    # Find contours
    

    contours, _ = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) >= 65]
    #cv2.drawContours(segmented_img, filtered_contours, -1, (0, 0, 255), 2)

    
    big_contour = get_contour_with_largest_height(contours)
    _, y, _, h = cv2.boundingRect(big_contour)
    
    contours_map = {}
    for contour in filtered_contours:        
        min_y, max_y = get_contour_y_range(contour)
        
        key = (min_y, max_y)  # Use a tuple as the key
        
        if key in contours_map:
            contours_map[key] += 1
        else:
            contours_map[key] = 1
            

    noise_line = max(contours_map, key=contours_map.get)
    
    segmented_img_per_noise = segmented_img[noise_line[1]:y+h, :]
    
    if show_image:
        Prints.show_img(segmented_img_per_noise)
    
    return segmented_img_per_noise


    