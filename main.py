from pnuidmapper import Mapper as mp 
from avg_training_pnu import PNUMatcher as pnm 
from plotPnuIdHist import ImagePNUIDHistogram as ipnuidHis

DB = './Data-Base'
IDS = [x for x in range(3)]
BASE_DIRECTORY = '/home/ameer/img-camera-matching/Data-Base'
DATA_DUMP = '/home/ameer/img-camera-matching/Data-Base/results/'


if __name__ == '__main__':
    mp = mp(DB,1)
    mp.transform_all_imges()
    mp.create_ID().saveID()
    matcher = pnm(BASE_DIRECTORY, DATA_DUMP)
    matcher.calculate_correlation()
    matcher.save_results()
                