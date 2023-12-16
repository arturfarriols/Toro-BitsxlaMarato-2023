import cv2
import matplotlib.pyplot as plt
import numpy as np
import PIL

from utils import *

MAX_FREQUENCY = 220
MIN_FREQUENCY = 40
DIFFERENCE = MAX_FREQUENCY - MIN_FREQUENCY

def show_img(img, use_open_cv:bool = False):
    if use_open_cv:
        cv2.imshow("image", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.title("Image")
        plt.axis('off')  # Hide axis labels and ticks
        plt.show()

def segment_colors(img):
    green_segmented_img = segment_green(img)
    red_segmented_img = segment_red(img)
    black_segmented_img = detect_and_paint(img) #segment_black(img)

    return green_segmented_img, red_segmented_img, black_segmented_img

def preprocess_image(image):
    # Apply dilation to make the gray parts thicker
    dilated_image = cv2.dilate(image, np.ones((5, 5), np.uint8), iterations=4)

    # Apply erosion to return to the original size
    eroded_image = cv2.erode(dilated_image, np.ones((5, 5), np.uint8), iterations=4)

    return eroded_image

def get_contour_extremes(contour):
    if len(contour) == 0:
        return None, None

    # Initialize with the first point
    min_y = max_y = contour[0][0][1]

    # Iterate through the contour points
    for point in contour:
        y = point[0][1]
        min_y = min(min_y, y)
        max_y = max(max_y, y)

    return min_y, max_y

def get_contour_with_largest_area(contours):
    if not contours:
        return None

    # Find the contour with the largest area
    max_contour = max(contours, key=cv2.contourArea)

    return max_contour

def get_contours(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # _, thresholded = cv2.threshold(gray_img, 128, 255, cv2.THRESH_BINARY)
    processed_image = preprocess_image(gray_img)
    contours, _ = cv2.findContours(processed_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    image_with_contours = cv2.cvtColor(gray_img, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(image_with_contours, contours, -1, (0, 255, 0), 2)

    # show_img(processed_image, use_open_cv=False)
    # show_img(image_with_contours, use_open_cv=False)

    return contours, image_with_contours

def get_freq_to_pixel_ratio(img, segmented_img):
    # segmented_img = segment_green(img)
    contours, image_with_contours = get_contours(segmented_img)
    biggest_contour = get_contour_with_largest_area(contours)
    extremes = get_contour_extremes(biggest_contour)
    
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

if __name__ == "__main__":
    img_path = "img2.png"

    img = cv2.imread(img_path)

    # print(np.unique(img))
    print(img[0])
    print(img[0, 2000])

    green_segmented_img, red_segmented_img, black_segmented_img = segment_colors(img)

    print(np.shape(img))
    # show_img(img, use_open_cv=False)
    # show_img(segmented_img, use_open_cv=False)

    min, max, ratio = get_freq_to_pixel_ratio(img, green_segmented_img)

    show_img(green_segmented_img, use_open_cv=False)
    show_img(red_segmented_img, use_open_cv=False)
    show_img(black_segmented_img, use_open_cv=False)


    print(min, max, ratio)
    
    

    
