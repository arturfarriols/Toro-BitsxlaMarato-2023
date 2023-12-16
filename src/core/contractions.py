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
    
