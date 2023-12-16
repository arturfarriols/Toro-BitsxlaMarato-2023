import cv2
import numpy as np



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


def preprocess_image(image):
    # Apply dilation to make the gray parts thicker
    dilated_image = cv2.dilate(image, np.ones((5, 5), np.uint8), iterations=4)

    # Apply erosion to return to the original size
    eroded_image = cv2.erode(dilated_image, np.ones((5, 5), np.uint8), iterations=4)

    return eroded_image
