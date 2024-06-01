import numpy as np
import pywt
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import dataBase as db
import imgReader as ir


class WVT:
    def __init__(self, img : np.array):
        self.img = img
        self.coeffs2 = None 
        self.LL,self.LH, self.HL, self.HH = None,None,None,None 
        self.Transform()
    
    def Transform(self):
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

    def get_HH(self):
        return self.HH 
        
if __name__ == "__main__":
    # Example usage
    db = db.DataBase('./Data-Base')
    img_reader = ir.ImgReader(db.db_index_path(2))
    # Perform wavelet transformation
    wvt = WVT(img_reader.get_image_data(300))
    # Plot the four parts of the transformation

    wvt.plot_transformation()
