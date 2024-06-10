import numpy as np 

def correlation(img1: np.array, img2: np.array):
    flat1 = img1.flatten()
    flat2 = img2.flatten()
    return np.corrcoef(flat1, flat2)[0, 1]
    