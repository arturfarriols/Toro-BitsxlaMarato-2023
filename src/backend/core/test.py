from contractions import *
from cardiac_frequency import *



if __name__ == "__main__":
    img_path = "img7.png"

    img = cv2.imread(img_path)


    green_segmented_img, red_segmented_img, black_segmented_img = Segmentation.segment_colors(img)

    min, max_value, ratio = get_freq_to_pixel_ratio(img, green_segmented_img)

    print(min, max_value, ratio)

    
    mean, is_FCFB_determined, img_mean, variability, amount_accelerations, amount_decelerations = analyze_red_line(red_segmented_img, min, max_value, ratio)

    

    print(mean)
    print(get_contractions_per_ranges(img,ratio))
            
    