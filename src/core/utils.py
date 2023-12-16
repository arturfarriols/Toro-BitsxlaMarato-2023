import cv2
import numpy as np

def segment_green(image):
    # Convert the image from BGR to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds for the green color in HSV
    lower_green = np.array([40, 40, 40])  # Adjust these values based on your specific case
    upper_green = np.array([80, 255, 255])  # Adjust these values based on your specific case

    # Create a mask using the inRange function to segment the green color
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Apply the mask to the original image to get the segmented green values
    result = cv2.bitwise_and(image, image, mask=mask)

    return result

def segment_red(image):
    # Convert the image from BGR to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds for the red color in HSV
    lower_red1 = np.array([0, 100, 100])  # Adjust these values based on your specific case
    upper_red1 = np.array([10, 255, 255])  # Adjust these values based on your specific case
    lower_red2 = np.array([160, 100, 100])  # Adjust these values based on your specific case
    upper_red2 = np.array([180, 255, 255])  # Adjust these values based on your specific case

    # Create masks using the inRange function to segment the red color
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    # Combine masks to get the final mask for red color
    mask_red = cv2.bitwise_or(mask1, mask2)

    # Apply the mask to the original image to get the segmented red values
    result_red = cv2.bitwise_and(image, image, mask=mask_red)

    return result_red

def segment_black(img):
    # Convert the image to HSV color space
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds for black color in HSV
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([0, 0, 0]) #180, 255, 30
    white = np.array([255, 255, 255])

    # Create a mask using the inRange function to segment the black color
    mask_black = cv2.inRange(img, white, white)

    # Apply the mask to the original image to get the segmented black values
    result_black = cv2.bitwise_and(img, img, mask=mask_black)

    return result_black

def detect_and_paint(image):
    # Create a mask for pixels with values (0, 0, 0)
    mask_black = np.all(image == [0, 0, 0], axis=-1)

    # Create a white image
    white_image = np.ones_like(image) * 255

    # Paint pixels with values (0, 0, 0) black in the white image
    white_image[mask_black] = image[mask_black]

    return white_image