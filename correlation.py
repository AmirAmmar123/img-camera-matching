import numpy as np 

def correlation(pnu_x: np.array,n: np.array):
    """
    Calculates the correlation between two arrays based on the formula: 
    np.dot(n - n^, pnu_x - pnu_x^) / (norm(n - n^) * norm(pnu_x - pnu_x^)). 
    Where:
    - n is the wave-transform F(n).
    - n^ is the average of the image, obtained by applying the inverse wave-transform to F(n).
    - pnu_x is the pnu_id of the set x.
    - pnu_x^ is the average of pnu_id values in the set x.

    Returns the correlation value between the two arrays.
    """
    """ 
        np.dot(n-n^, pnu_x - pnu_x^) /( norm(n-n^) * norm(pnu_x - pnu_x^) ) 
        n  = the F(n), F is wave-transform 
        n^ = the average( image ),   image=F**-1( F(n) ) 
        pnu_x = pnu_id of the set x 
        pnu_x^ = average of (pnu_id)
        
    """
    n_gag = np.average(n)
    pnu_x_gag = np.average(pnu_x)
    flat_image1 = (n - n_gag).flatten()
    flat_image2 = (pnu_x - pnu_x_gag).flatten()
    return np.corrcoef(flat_image1, flat_image2)[0,1]
