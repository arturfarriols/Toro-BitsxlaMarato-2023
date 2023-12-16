from contractions import *
from cardiac_frequency import *



if __name__ == "__main__":
    img_path = "img5.png"

    img = cv2.imread(img_path)

    # print(np.unique(img))
    print(img[0])
    print(img[0, 2000])

    green_segmented_img, red_segmented_img, black_segmented_img = Segmentation.segment_colors(img)

    print(np.shape(img))
    
    # show_img(img, use_open_cv=False)
    # show_img(segmented_img, use_open_cv=False)

    min, max_value, ratio = get_freq_to_pixel_ratio(img, green_segmented_img)

    print(min, max_value, ratio)
    print("Contractions ranges:", get_contractions_ranges(img, show_image=False))
    print(min, max_value, ratio)
    

    
    