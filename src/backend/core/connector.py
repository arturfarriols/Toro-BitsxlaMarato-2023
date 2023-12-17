from . import Contractions
from . import Cardiac
import cv2
import os
import uuid
# Get the current working directory


def analyize(img_path):
    
    current_directory = os.getcwd()
    absolute_path = os.path.join(current_directory, "data/data-hackaton", img_path)
    img = cv2.imread(absolute_path)

    green_segmented_img, red_segmented_img, black_segmented_img = Cardiac.utils.Segmentation.segment_colors(img)

    min, max_value, ratio = Cardiac.get_freq_to_pixel_ratio(img, green_segmented_img)
    print(min, max_value, ratio)

    
    mean, is_FCFB_determined, img_mean, variability, amount_accelerations, amount_decelerations = Cardiac.analyze_red_line(red_segmented_img, min, max_value, ratio)
    random_uuid = str(uuid.uuid4()) + ".png"

    save_path = os.path.join(current_directory, "src/frontend/public", random_uuid)
    cv2.imwrite(save_path, img_mean)
    contractions = Contractions.get_contractions_per_ranges(img,ratio)
    return contractions, mean, is_FCFB_determined, random_uuid, variability, amount_accelerations, amount_decelerations