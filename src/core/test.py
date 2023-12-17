from contractions import *
from cardiac_frequency import *



if __name__ == "__main__":
    img_path = "img2.png"

    img = cv2.imread(img_path)


    green_segmented_img, red_segmented_img, black_segmented_img = Segmentation.segment_colors(img)

    min, max_value, ratio = get_freq_to_pixel_ratio(img, green_segmented_img)

    print(min, max_value, ratio)
    
    ranges = get_contractions_ranges(img, show_image=False)
    print("Contractions ranges:", ranges)
    print(min, max_value, ratio)
    
    mean, is_FCFB_determined, img_mean, variability, amount_accelerations, amount_decelerations = analyze_red_line(red_segmented_img, min, max_value, ratio)

    

    print(mean)
    for i in range(len(ranges)):
        if i+1 < len(ranges):
            contraction_img = get_contractions_per_range(img, ranges[i],ranges[i+1], False)
            mean, img_mean, number_of_contractions = get_contractions(contraction_img, ratio)
            print(mean)
            print(number_of_contractions)
            Prints.show_img(img=img_mean)
            
    