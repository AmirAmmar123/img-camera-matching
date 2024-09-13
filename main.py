from pnuidmapper import Mapper as mp 
from Plotting.plotPnuIdHist import ImagePNUIDHistogram as ipnuidHis
from avg_training_pnu import PNUMatcher as pnm 
from optimized_averging_training_pnu import PNUMatcher as opnm
from preparing_data_for_gaussian_thresholding import DataProcessor as dp 
import json 
from joinData import AllData, DATABASE_PATH
from gussian import TwoGussian, PNU
import os 

NUM_CAMERAS = 6 
CAMERA_SET_ID = [x for x in range(NUM_CAMERAS)]
BASE_DIRECTORY = 'img-camera-matching/Data-Base'
DATA_DUMP = '/data-base/results/'
READ_RESULTS= "data-base/results/data.json"
WRITE_SORTED= "data-base/results/preparing_to_thresholding.json"
READ_SORTED = WRITE_SORTED 
READ_SORTED = "/home/ameer/img-camera-matching/data-base/results/preparing_to_thresholding.json"

if __name__ == '__main__':
    # mp = mp(DATABASE_PATH,CAMERA_SET_ID[4])
    # mp.transform_all_imges()
    # mp.create_ID().saveID()
    # matcher = opnm(BASE_DIRECTORY, DATA_DUMP)
    # matcher.calculate_correlation()
    # matcher.save_results()
    # staged = dp(READ_RESULTS, WRITE_SORTED)
    # staged.run()
    
    all_data = AllData(DATABASE_PATH)
    all_data.join()
    all_data.map_to_imges()
    # Load the JSON data
    with open(READ_SORTED, 'r') as file:
        data = json.load(file)
    
    gussians = []
    for x,v in data.items():
        path1, path2 = v.keys()
        path_to_pnu = os.path.dirname(x) + PNU
        path_to_the_Highest = os.path.dirname(path2)
        path_to_second_eighest = os.path.dirname(path1)
        gussians.append(TwoGussian(path_to_pnu, path_to_the_Highest, path_to_second_eighest))
    
    for g in gussians:
        g.init_data(all_data)
    print(gussians)
    