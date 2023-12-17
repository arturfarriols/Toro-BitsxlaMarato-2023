import cv2
import matplotlib.pyplot as plt
import numpy as np
import PIL

from . import utils


def get_contractions_ranges(img, show_image:bool=False):
    green_segmented_img = utils.Segmentation.segment_green(img)
    
    contours, _ = utils.Contours.get_contours(green_segmented_img)
    max_contour = max(contours, key=lambda cnt: cv2.boundingRect(cnt)[1])
    
    _, y, _, h = cv2.boundingRect(max_contour)
    
    # Find all pixels with y-coordinate greater than or equal to max_contour's y-coordinate
    selected_points = [[i, j] for point in max_contour for i, j in [point[0]] if j >= y + h - 1]

            
    if len(selected_points)%2 != 0:
        print("ERROR: Getting contractions range!!!!!")
    
    ranges = [int((p1[0] + p2[0]) / 2) for p1, p2 in zip(selected_points[::2], selected_points[1::2])]
    
    if show_image:
        utils.Prints.print_img_per_x_and_show(green_segmented_img, ranges)
    
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
    
    black_segmented_img = utils.Segmentation.detect_and_paint(img)
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

def get_contractions(img, ratio):
    threshold = -20 * ratio
    number_of_contractions = 0

    black_pixels = find_black_pixels(img)
    # divided_black_pixels = divide_into_contiguous_subdictionaries(black_pixels)
    mean = calculate_mean(black_pixels)
    # print("threshold", threshold)
    img_mean = draw_horizontal_line(img, int(mean))

    # print(np.shape(img))
    # Prints.show_img(img_mean, use_open_cv=False)
    # print(mean)
    # print(np.unique(list(black_pixels.values())))
    # print(len(divided_black_pixels))
    values = list(black_pixels.values())
    is_contraction = False

    for value in values:
        if value < mean + threshold and not is_contraction:
            is_contraction = True
            number_of_contractions += 1
        elif value >= mean + threshold and is_contraction:
            is_contraction = False

    return mean / ratio, img_mean, number_of_contractions

def calculate_mean(dictionary):
    if not dictionary:
        return None
    
    values = list(dictionary.values())
    mean = np.mean(values)
    return mean

def draw_horizontal_line(image, y_coordinate, color=(0, 0, 255), thickness=2):
    # Clone the image to avoid modifying the original
    image_with_line = image.copy()

    # Get the width of the image
    width = image_with_line.shape[1]

    # Draw a horizontal line
    cv2.line(image_with_line, (0, y_coordinate), (width, y_coordinate), color, thickness)

    return image_with_line

def divide_into_contiguous_subdictionaries(dictionary, max_gap=1):
    if not dictionary:
        return []

    sorted_keys = sorted(dictionary.keys())
    subdictionaries = []

    current_subdict = {sorted_keys[0]: dictionary[sorted_keys[0]]}
    previous_key = sorted_keys[0]
    for key in sorted_keys[1:]:
        if key - max_gap > previous_key:
            subdictionaries.append(current_subdict)
            current_subdict = {key: dictionary[key]}
        else:
            current_subdict[key] = dictionary[key]
        previous_key = key

    subdictionaries.append(current_subdict)
    return subdictionaries

def find_black_pixels(binary_image):
    middle_black_pixels = {}  # Dictionary to store column number and middle white pixel y-coordinate

    # Iterate over each column
    for col in range(binary_image.shape[1]):
        # Extract the column
        column = binary_image[:, col]

        # Find the white pixels (pixel value = 255)
        black_pixels = np.where(column == 0)[0]

        if len(black_pixels) > 0:
            # Find the middle white pixel
            middle_pixel_index = black_pixels[len(black_pixels) // 2]
            middle_pixel_y = middle_pixel_index

            # Store in the dictionary
            middle_black_pixels[col] = middle_pixel_y

    return middle_black_pixels

def get_contractions_per_ranges(img, ratio):
    ranges = get_contractions_ranges(img, show_image=False)
    print("Contractions ranges:", ranges)
    
    contractions_per_ranges = []
    for i in range(len(ranges)):
        if i+1 < len(ranges):
            contraction_img = get_contractions_per_range(img, ranges[i],ranges[i+1], False)
            mean, img_mean, number_of_contractions = get_contractions(contraction_img, ratio)
            #Prints.show_img(img=img_mean)
            contractions_per_ranges.append(number_of_contractions)
    return contractions_per_ranges