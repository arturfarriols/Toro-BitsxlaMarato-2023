from contractions import *
from cardiac_frequency import *



if __name__ == "__main__":
    img_path = "img7.png"

    img = cv2.imread(img_path)


    green_segmented_img, red_segmented_img, black_segmented_img = Segmentation.segment_colors(img)

    min, max_value, ratio = get_freq_to_pixel_ratio(img, green_segmented_img)

    print(min, max_value, ratio)
    
    ranges = get_contractions_ranges(img, show_image=False)
    print("Contractions ranges:", ranges)
    print(min, max_value, ratio)
    
    for i in range(len(ranges)):
        if i+1 < len(ranges):
            get_contractions_per_range(img, ranges[i],ranges[i+1])
    