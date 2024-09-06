from pnuidmapper import Mapper as mp 
from avg_training_pnu import PNUMatcher as pnm 
from plotPnuIdHist import ImagePNUIDHistogram as ipnuidHis
from optimized_averging_training_pnu import PNUMatcher as opnm


if __name__ == '__main__':
    NUM_CAMERAS = 5 
    DB = './Data-Base'
    CAMERA_ID = [x for x in range(NUM_CAMERAS)]
    BASE_DIRECTORY = '/home/ameer/img-camera-matching/Data-Base'
    DATA_DUMP = '/home/ameer/img-camera-matching/Data-Base/results/'

    # mp = mp(DB,CAMERA_ID[3])
    # mp.transform_all_imges()
    # mp.create_ID().saveID()
    matcher = opnm(BASE_DIRECTORY, DATA_DUMP)
    matcher.calculate_correlation()
    matcher.save_results()
                