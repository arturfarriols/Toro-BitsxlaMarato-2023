import cv2
import matplotlib.pyplot as plt
import numpy as np
import PIL

from utils import *

MAX_FREQUENCY = 220
MIN_FREQUENCY = 40
DIFFERENCE = MAX_FREQUENCY - MIN_FREQUENCY

def get_freq_to_pixel_ratio(img, segmented_img):
    # segmented_img = segment_green(img)
    contours, image_with_contours = Contours.get_contours(segmented_img)
    biggest_contour = Contours.get_contour_with_largest_area(contours)
    extremes = Contours.get_contour_extremes(biggest_contour)
    
    print(extremes)
    amount_of_pixels = extremes[1] - extremes[0]
    ratio = amount_of_pixels/ DIFFERENCE
    return extremes[0], extremes[1], ratio

    # point1 = (400, extremes[0])
    # point2 = (400, extremes[1])
    # # Draw circles at the specified points
    # radius = 8
    # color = (255, 0, 0)  # Green color in BGR
    # thickness = -1  # Filled circle
    # cv2.circle(img, point1, radius, color, thickness)
    # cv2.circle(img, point2, radius, color, thickness)    
