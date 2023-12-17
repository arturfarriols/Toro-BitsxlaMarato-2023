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
