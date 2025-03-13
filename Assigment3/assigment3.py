import cv2
import numpy as np
from matplotlib import pyplot as plt
from skimage.filters import threshold_multiotsu


def otsu2class(image):    
    """Applies Otsu's thresholding for binary (2-class) segmentation."""
    _, binary_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary_image

def multiotsu(image):
    """Applies Multi-Otsu thresholding for multi-class segmentation."""
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresholds = threshold_multiotsu(gray_image)
    segmented_image = np.digitize(gray_image, bins=thresholds)
    return segmented_image


def mean_shift(image, spatial_radius=15, color_radius=30):
    """Applies Mean Shift filtering to an image."""
    return cv2.pyrMeanShiftFiltering(image, sp=spatial_radius, sr=color_radius)

def processing(images):
    processed_images = [
        multiotsu(images[0]),  # Multi-Otsu
        otsu2class(images[1]),  # Otsu 2-Class
        mean_shift(images[2]),  # Mean Shift Filtering
    ]

    results = images + processed_images     
    titles = ["Otsu Multiclass", "Binary Otsu", "Mean Shift"]

    for i in range(3):
        results[i] = cv2.cvtColor(image_list[i], cv2.COLOR_BGR2RGB)
        if i==2:
            results[i+3] = cv2.cvtColor(results[i+3], cv2.COLOR_BGR2RGB)
        plt.subplot(2,3,i+1), plt.imshow(results[i])
        plt.title("Original"), plt.xticks([]), plt.yticks([])
        plt.subplot(2,3,i+4), plt.imshow(results[i+3], cmap= 'gray')
        plt.imsave(f"{titles[i]}.png", results[i+3], cmap = 'gray')
        plt.title(titles[i]), plt.xticks([]), plt.yticks([])
    plt.show()

    
if __name__ == "__main__":
    image_files = ['OTSU Multiple Class-S01-150x150.png', 'OTSU2class-edge_L-150x150.png', 'meanshift S00-150x150.png']
    image_list = []
    for img_file in image_files:
        img_path = "Assigment3/Images/" + img_file
        if "OTSU2" in img_file:
            image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        else:
            image = cv2.imread(img_path)
        image_list.append(image)
    
    processing(image_list)