import cv2
import matplotlib.pyplot as plt
import numpy as np
import PIL

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
        
def print_img_per_x_and_show(img, ranges, color=[0,0,255], use_open_cv:bool = False):
    for x_value in ranges:
        for _, col in enumerate(img):
            col[x_value] = color

    show_img(img,use_open_cv)