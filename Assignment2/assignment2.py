import cv2
import numpy as np

def show_image(image_path):
    # Load the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    print(image.dtype)
    
    # Check if image was successfully loaded
    if image is None:
        print("Error: Could not read the image.")
        return
    
    # Display the image
    #cv2.imshow('Image', image)
    boxNoCV(image)

    
    # Wait for a key press and close the window
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

def boxNoCV(image):
    mask3 = np.ones((3,3),np.float32)/9

    rows = image.shape[0]
    cols = image.shape[1]

    blurred = np.zeros((rows,cols), np.uint8)

    #grab first 3 rows and first 3 columns

    for row in range(rows-2):
        for col in range(cols-2):
            region = image[row:row + 3, col:col + 3]
            value = 0

            value = np.sum(region * mask3)
            blurred[row, col] = value
    
    cv2.imshow('Image', blurred)
    #print(blurred)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    mask5 = np.ones((5,5),np.float32)/25




# Example usage
if __name__ == "__main__":
    image_path = "Assignment2/dog.bmp"  # Replace with the path to your image
    show_image(image_path)
