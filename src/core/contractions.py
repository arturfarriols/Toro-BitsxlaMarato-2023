import cv2
import matplotlib.pyplot as plt
import numpy as np
import PIL

from utils import *


def get_contractions_ranges(img, show_image=False):
    green_segmented_img = Segmentation.segment_green(img)
    
    contours, _ = Contours.get_contours(green_segmented_img)
    max_contour = max(contours, key=lambda cnt: cv2.boundingRect(cnt)[1])
    
    _, y, _, h = cv2.boundingRect(max_contour)
    
    # Find all pixels with y-coordinate greater than or equal to max_contour's y-coordinate
    selected_points = []
    
    for point in max_contour:
        i,j = point[0]
        if j >= y+h-1:
            print("x:", i, "y:", j)
            green_segmented_img[j,i] = [0,0,255] 
            selected_points.append([i, j])
            
    if len(selected_points)%2 != 0:
        print("ERROR: Getting contractions range!!!!!")
    
    ranges = []
    
    for i in range(0, len(selected_points), 2):
        print(i, selected_points[i], selected_points[i+1])
        x_mean = int((selected_points[i][0]+selected_points[i+1][0])/2)
        ranges.append(x_mean)

    
    
    if(show_image):
        for x_value in ranges:
            for row in range(len(green_segmented_img)):
                for col in range(len(green_segmented_img[row])):
                    if col == x_value:
                        green_segmented_img[row][col] = [0, 0, 255]
        Prints.show_img(green_segmented_img)
    
    return ranges
    
