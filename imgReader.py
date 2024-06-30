
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
from pillow_heif import register_heif_opener
import os
import numpy

# Register HEIF opener for PIL
register_heif_opener()

class ImgReader:
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

    def __init__(self, path : str):
        """
        Initializes the ReadImages class with the specified directory path.

        Args:
            path (str): The directory path containing the image files.
        """
        self.path = path
        self.collection = self.getImages(self.path)

    @staticmethod
    def getImages(path: str):
        """
        Static method to retrieve a list of image filenames from the given directory path.

        Args:
            path (str): The directory path containing the image files.

        Returns:
            list: A list of image filenames with supported extensions => (.png .jpg .jpeg .heic)
        """
        image_filenames = os.listdir(path)
        
        return [filename for filename in image_filenames if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.heic'))]

    def read_image_path(self, index : int):
        """
        Returns the full path of the image file at the specified index in the collection.

        Args:
            index (int): The index of the image file in the collection.

        Returns:
            str: The full path of the image file.
        """
        return f'{self.path}/{self.collection[index]}'
    
    def get_image_data(self, index : int) -> numpy.array:
        img_path = self.read_image_path(index)
        img = mpimg.imread(img_path)
        
        # Convert to grayscale if necessary
        if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        return img
    
    def get_collection_size(self) -> int :
        return len(self.collection)

    def plot_image(self, img: numpy.array):
        plt.figure(figsize=(4, 4), dpi=100) 
        plt.imshow(img, cmap=plt.cm.gray)
        plt.axis('off') 
        plt.show()

    def getSetImagePath(self) -> str:
        return self.path
