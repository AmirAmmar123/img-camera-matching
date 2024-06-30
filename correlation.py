import numpy as np 

def correlation(pnu_x: np.array,n: np.array):
    """ 
        np.dot(n-n^, pnu_x - pnu_x^) /( norm(n-n^) * norm(pnu_x - pnu_x^) ) 
        n  = the F(n), F is wave-transform 
        n^ = the average( image ),   image=F**-1( F(n) ) 
        pnu_x = pnu_id of the set x 
        pnu_x^ = average of (pnu_id)
        
    """
    n_gag = np.average(n)
    pnu_x_gag = np.average(pnu_x)
    return np.dot(n - n_gag, pnu_x - pnu_x_gag)/(np.linalg.norm(n - n_gag) * np.linalg.norm(pnu_x - pnu_x_gag))
    
    
    
    # threshold = {test(set) -> succession}
    # accuracy