import numpy as np
import matplotlib.pyplot as plt
import tifffile as tiff
from skimage import exposure
import os

class ImagePNUIDHistogram:
    def __init__(self, image_path: str, save_dir: str = None):
        """
        Initializes the ImagePNUIDHistogram class with an image path and an optional save directory.
        
        Args:
        image_path (str): Path to the image file.
        save_dir (str): Directory where the histogram and image will be saved. Default is None.
        """
        self.image_path = image_path
        self.save_dir = save_dir
        self.image = self._load_image()
    
    def _load_image(self) -> np.array:
        """
        Loads the image from the specified path.
        
        Returns:
        np.array: Loaded image.
        """
        return tiff.imread(self.image_path)
    
    def plot_histogram(self, save: bool = False):
        """
        Calculates and plots the histogram of the loaded image using skimage's exposure.histogram.
        Optionally saves the histogram plot.
        """
        # Calculate the histogram
        histogram, bins = exposure.histogram(self.image)
        
        # Plot the histogram
        plt.figure()
        plt.title(f'PNU id Histogram for {self.image_path}')
        plt.xlabel("Bins")
        plt.ylabel("# of Pixels")
        plt.bar(bins, histogram, width=1)
        plt.xlim([-5, 5])  # Adjusted to match the range of grayscale values
        
        if save and self.save_dir:
            res = ''.join(self.image_path.split('/')[2:-2])
            histogram_path = os.path.join(self.save_dir, f'{res}_histogram.png')
            plt.savefig(histogram_path)
            print(f'Histogram saved as {histogram_path}')
        else:
            plt.show()
    
    def show_image(self, save: bool = False):
        """
        Displays the loaded image. Optionally saves the image.
        """
        plt.figure()
        plt.title("Image")
        plt.imshow(self.image, cmap='gray')
        plt.axis('off')  # Hide axes
        
        if save and self.save_dir:
            res = ''.join(self.image_path.split('/')[2:-2])
            image_path = os.path.join(self.save_dir, os.path.join(self.save_dir, f'{res}_histogram.png'))
            plt.savefig(image_path, bbox_inches='tight', pad_inches=0)
            print(f'Image saved as {image_path}')
        else:
            plt.show()

if __name__ == "__main__":
    PATH = './data-base/'
    IMG = 'pnu_id.tiff'
    DIR = '/pnu_id/'
    SAVE_DIR = './plots/'
    
    # Ensure the save directory exists
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
    
    dirs = os.listdir(PATH)
    dirs = [f'{PATH}{dir}{DIR}{IMG}' for dir in dirs if os.path.exists(f'{PATH}{dir}{DIR}{IMG}')]
    for path in dirs:
        hist = ImagePNUIDHistogram(path, save_dir=SAVE_DIR)
        hist.plot_histogram(save=True)
