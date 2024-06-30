from ctypes import Array
from typing import Any
import numpy as np
import pywt
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import dataBase as db
import imgReader as ir


class WVT:
    """
    Transforms the image using wavelet transform.

    Args:
        self: The instance of the class.

    """


    WIDTH, HEIGHT = 3024, 4032 
    SHAPE = (HEIGHT, WIDTH)
    
    def __init__(self, img : np.array):
        self.img = img
        self.coeffs2 = None 
        self.LL,self.LH, self.HL, self.HH = None,None,None,None 
        self.Transform()
    
    def Transform(self)-> None:
        """
        Transforms the image using wavelet transform.

        Args:
            self: The instance of the class.
            
        """
        if self.img.shape != self.SHAPE:
            self.img = self.img.T
        self.coeffs2 = pywt.dwt2(self.img, 'bior1.3')
        self.LL, (self.LH, self.HL, self.HH) = self.coeffs2
    
    # reminder sized may differ after the transportation due to the nature size of the images in each directory
    def plot_transformation(self):    
        fig = plt.figure(figsize=(12, 3))
        titles = ['Approximation', ' Horizontal detail',
            'Vertical detail', 'Diagonal detail']
        for i, a in enumerate([self.LL, self.LH, self.HL, self.HH]):
            ax = fig.add_subplot(1, 4, i + 1)
            ax.imshow(a, interpolation="nearest", cmap=plt.cm.gray)
            ax.set_title(titles[i], fontsize=10)
            ax.set_xticks([])
            ax.set_yticks([])

        fig.tight_layout()
        plt.show()

    def get_HH(self)-> (Any | Array | None):
        """
        Returns the HH component of the wavelet transformation.

        Args:
            self: The instance of the class.

        Returns:
            The HH component of the wavelet transformation.
        """
        return self.HH 
        
if __name__ == "__main__":
    # Example usage
    db = db.DataBase('./Data-Base')
    img_reader = ir.ImgReader(db.db_index_path(2))
    # Perform wavelet transformation
    wvt = WVT(img_reader.get_image_data(300))
    # Plot the four parts of the transformation

    wvt.plot_transformation()
