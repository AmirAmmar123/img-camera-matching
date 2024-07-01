import cv2
import numpy as np
import matplotlib.pyplot as plt
import tifffile as tiff
from skimage import exposure

class ImageHistogram:
    def __init__(self, image_path: str):
        """
        Initializes the ImageHistogram class with an image path.
        
        Args:
        image_path (str): Path to the image file.
        """
        self.image_path = image_path
        self.image = self._load_image()
    
    def _load_image(self) -> np.array:
        """
        Loads the image from the specified path.
        
        Returns:
        np.array: Loaded image.
        """

        return tiff.imread(self.image_path)
    
    def plot_histogram(self):
        """
        Calculates and plots the histogram of the loaded image using skimage's exposure.histogram.
        """
        # Calculate the histogram
        histogram, bins = exposure.histogram(self.image)
        
        # Plot the histogram
        plt.figure()
        plt.title("Grayscale Histogram")
        plt.xlabel("Bins")
        plt.ylabel("# of Pixels")
        plt.bar(bins, histogram, width=1)
        plt.xlim([-5, 5])  # Adjusted to match the range of grayscale values
        plt.show()
    
    def show_image(self):
        """
        Displays the loaded image.
        """
        plt.figure()
        plt.title("Image")
        plt.imshow(self.image, cmap='gray')
        plt.axis('off')  # Hide axes
        plt.show()

