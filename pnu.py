import os
from PIL import Image
import numpy as np
from pillow_heif import register_heif_opener
import pywt
import matplotlib.pyplot as plt
import cv2 

register_heif_opener()

class ReadImages:
    """
    A class for reading image files from a specified directory.

    Attributes:
        path (str): The directory path containing the image files.
        collection (list): A list of image filenames in the directory.

    Methods:
        __init__(path): Initializes the ReadImages class with the specified directory path.
        getImages(path): Static method to retrieve a list of image filenames from the given directory path.
        read_image_path(index): Returns the full path of the image file at the specified index in the collection.
    """

    def __init__(self, path):
        """
        Initializes the ReadImages class with the specified directory path.

        Args:
            path (str): The directory path containing the image files.
        """
        self.path = path
        self.collection = ReadImages.getImages(self.path)

    @staticmethod
    def getImages(path):
        """
        Static method to retrieve a list of image filenames from the given directory path.

        Args:
            path (str): The directory path containing the image files.

        Returns:
            list: A list of image filenames with supported extensions.
        """
        # List all files in the directory
        image_filenames = os.listdir(path)
        # Filter out only the image files (you can customize this based on your file extensions)
        return [filename for filename in image_filenames if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.heic'))]

    def read_image_path(self, index):
        """
        Returns the full path of the image file at the specified index in the collection.

        Args:
            index (int): The index of the image file in the collection.

        Returns:
            str: The full path of the image file.
        """
        return f'{self.path}/{self.collection[index]}'

if __name__ == "__main__":
    # Example usage
    path_ = './Data-Base/iphone14-pro'
    img_reader = ReadImages(path_)
    image = Image.open(img_reader.read_image_path(5))
    data = np.array(image, dtype=float)
    
    # Perform a 2D wavelet decomposition on the image
    coeffs = pywt.dwt2(data, 'bior1.3')
    LL, (LH, HL, HH) = coeffs
    
    # Normalize coefficients for visualization
    LL_norm = cv2.normalize(LL, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    LH_norm = cv2.normalize(LH, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    HL_norm = cv2.normalize(HL, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    HH_norm = cv2.normalize(HH, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    
    # Plotting the wavelet coefficients
    titles = ['Approximation', 'Horizontal detail', 'Vertical detail', 'Diagonal detail']
    fig, axs = plt.subplots(2, 2, figsize=(12, 12))
    axs[0, 0].imshow(LL_norm, cmap='gray')
    axs[0, 0].set_title(titles[0])
    axs[0, 1].imshow(LH_norm, cmap='gray')
    axs[0, 1].set_title(titles[1])
    axs[1, 0].imshow(HL_norm, cmap='gray')
    axs[1, 0].set_title(titles[2])
    axs[1, 1].imshow(HH_norm, cmap='gray')
    axs[1, 1].set_title(titles[3])
    for ax in axs.flat:
        ax.axis('off')
    plt.tight_layout()
    plt.show()
