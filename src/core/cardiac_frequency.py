import cv2
import matplotlib.pyplot as plt
import numpy as np
import PIL
from scipy.stats import t

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

def draw_horizontal_line(image, y_coordinate, color=(0, 255, 0), thickness=2):
    # Clone the image to avoid modifying the original
    image_with_line = image.copy()

    # Get the width of the image
    width = image_with_line.shape[1]

    # Draw a horizontal line
    cv2.line(image_with_line, (0, y_coordinate), (width, y_coordinate), color, thickness)

    return image_with_line

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
    
    amount_of_pixels = extremes[1] - extremes[0]
    ratio = amount_of_pixels/ DIFFERENCE

    # show_img(image_with_contours, use_open_cv=False)

    return extremes[0], extremes[1], ratio

    # point1 = (400, extremes[0])
    # point2 = (400, extremes[1])
    # # Draw circles at the specified points
    # radius = 8
    # color = (255, 0, 0)  # Green color in BGR
    # thickness = -1  # Filled circle
    # cv2.circle(img, point1, radius, color, thickness)
    # cv2.circle(img, point2, radius, color, thickness)

def find_middle_red_pixels(binary_image):
    middle_white_pixels = {}  # Dictionary to store column number and middle white pixel y-coordinate

    # Iterate over each column
    for col in range(binary_image.shape[1]):
        # Extract the column
        column = binary_image[:, col]

        # Find the white pixels (pixel value = 255)
        white_pixels = np.where(column == 255)[0]

        if len(white_pixels) > 0:
            # Find the middle white pixel
            middle_pixel_index = white_pixels[len(white_pixels) // 2]
            middle_pixel_y = middle_pixel_index

            # Store in the dictionary
            middle_white_pixels[col] = middle_pixel_y

    return middle_white_pixels

def calculate_red_pixel_mean(dictionary):
    if not dictionary:
        return None
    
    values = list(dictionary.values())
    mean = np.mean(values)
    return mean

def calculate_confidence_interval(dictionary, confidence=0.95):
    if not dictionary:
        return None, None
    
    values = list(dictionary.values())
    n = len(values)
    mean = np.mean(values)
    std_dev = np.std(values, ddof=1) if n > 1 else 0
    
    # Calculate the margin of error
    margin_error = t.ppf((1 + confidence) / 2, n - 1) * (std_dev / np.sqrt(n))
    
    # Calculate the confidence interval
    lower_bound = mean - margin_error
    upper_bound = mean + margin_error
    
    return lower_bound, upper_bound

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

def calculate_mean_variance(dictionary):
    if not dictionary or len(dictionary) < 2:
        return None
    
    values = list(dictionary.values())
    mean_variance = 0
    number_of_elements = len(values)
    for i in range(1, number_of_elements):
        mean_variance += abs(values[i] - values[i - 1])
    mean_variance = mean_variance / number_of_elements
    # mean_variance = np.var(values, ddof=1)
    
    return mean_variance, number_of_elements

def calculate_percentage(array):
    if not array or len(array) == 0:
        return None

    total_sum = sum(array)
    percentages = [(value / total_sum) for value in array]

    return percentages

def multiply_and_sum_numpy(array1, array2):
    if not array1 or not array2 or len(array1) != len(array2):
        return None

    result = np.dot(array1, array2)
    return result

def get_accelerations(subdictionaries, mean, ratio):
    amount_of_accelerations = 0
    for dictionary in subdictionaries:
        if len(dictionary.keys()) > 50:
            amount_of_anomalous_values = 0
            for value in dictionary.values():
                if value > mean + 10 * ratio:
                    amount_of_anomalous_values += 1
                else:
                    if amount_of_anomalous_values > 5:
                        amount_of_accelerations += 1
                    amount_of_anomalous_values = 0
                
            if amount_of_anomalous_values > 5:
                amount_of_accelerations += 1
    return amount_of_accelerations

def get_decelerations(subdictionaries, mean, ratio):
    amount_of_decelerations = 0
    for dictionary in subdictionaries:
        if len(dictionary.keys())  > 50:
            amount_of_anomalous_values = 0
            for value in dictionary.values():
                if value < mean + 15 * ratio:
                    amount_of_anomalous_values += 1
                else:
                    if amount_of_anomalous_values > 15:
                        amount_of_decelerations += 1
                    amount_of_anomalous_values = 0
                
            if amount_of_anomalous_values > 15:
                amount_of_decelerations += 1
    return amount_of_decelerations

def analyze_red_line(img, min, max, ratio):
    grayscale_img = cv2.cvtColor(img[:max + 2], cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(grayscale_img, 1, 255, cv2.THRESH_BINARY)
    middle_red_pixels = find_middle_red_pixels(binary_image)

    subdictionaries = divide_into_contiguous_subdictionaries(middle_red_pixels)
    subdictionaries_mean_variace = 0
    amount_of_valid_subdictionaries = 0
    mean_variances = []
    number_of_elements = []
    for subdictionary in subdictionaries:
        mean_variace, elements = calculate_mean_variance(subdictionary)
        if mean_variace is not None and elements > 10:
            mean_variances.append(mean_variace)
            number_of_elements.append(elements)
            amount_of_valid_subdictionaries += 1

    percentages = calculate_percentage(number_of_elements)
    mean_variance = multiply_and_sum_numpy(mean_variances, percentages)

    mean = calculate_red_pixel_mean(middle_red_pixels)
    confidence_interval = calculate_confidence_interval(middle_red_pixels, confidence=0.95)

    is_FCFB_determined = abs(confidence_interval[1] - confidence_interval[1]) < 5

    if mean_variance <= 1.5:
        variability = "absent"
    elif 1.5 > mean_variance <= 3:
        variability = "reduced"
    elif 3 > mean_variance <= 4.5:
        variability = "normal"    
    else:
        variability = "augmented"

    amount_accelerations = get_accelerations(subdictionaries, mean, ratio)
    amount_decelerations = get_decelerations(subdictionaries, mean, ratio)

    # print(middle_red_pixels)
    print("mean", mean)
    print("mean_variance", mean_variance)
    print("amount_accelerations", amount_accelerations)
    print("amount_decelerations", amount_decelerations)

    img_mean = draw_horizontal_line(img.copy(), int(mean))

    return (abs(max - mean) / ratio) + MIN_FREQUENCY , is_FCFB_determined, img_mean, variability, amount_accelerations, amount_decelerations

if __name__ == "__main__":
    img_path = "img7.png"

    img = cv2.imread(img_path)

    green_segmented_img, red_segmented_img, black_segmented_img = segment_colors(img)

    print(np.shape(img))

    min, max, ratio = get_freq_to_pixel_ratio(img, green_segmented_img)
    print(min, max, ratio)
    # show_img(green_segmented_img, use_open_cv=False)
    # show_img(red_segmented_img, use_open_cv=False)
    # show_img(black_segmented_img, use_open_cv=False)

    mean, is_FCFB_determined, img_mean, variability, amount_accelerations, amount_decelerations = analyze_red_line(red_segmented_img, min, max, ratio)
    print(mean)
    show_img(img_mean, use_open_cv=False)

