import tifffile as tiff
import matplotlib.pyplot as plt
import os 
from correlation import correlation
from imgReader import ImgReader
from waveLetTransform import WVT
from plotHist import ImageHistogram
file_path = '/home/ameer/img-camera-matching/Data-Base/iphone14-pro/pnu_id/pnu_id.tiff'
pnu_x = tiff.imread(file_path)
# h = ImageHistogram(file_path)
# h.plot_histogram()
# h.show_image()

imr = ImgReader('/home/ameer/img-camera-matching/Data-Base/Iphone-13-Pro-Max-Model-Number-MLLE3HBA-Serial-Number-L36V45JK72/training/')
print(correlation(pnu_x,WVT(imr.get_image_data(30)).get_HH()))
 