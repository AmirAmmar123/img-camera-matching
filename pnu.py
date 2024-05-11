from skimage import io
import os
from PIL import Image
import numpy as np
from pillow_heif import register_heif_opener

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
    image = Image.open(img_reader.read_image_path(0))
    data = np.array(image, dtype=float)
    print(data.shape)
