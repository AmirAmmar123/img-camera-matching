from cameraImageMatcher import CameraImageMatcher
from loadGussian import LoadAllPairsOfGaussian, LoadGaussianPair
from const import GAUSSIANPLOTSTHEORY
from matplotlib import pyplot as plt 
import logging

logging.basicConfig(level=logging.INFO,  # Set level to INFO to capture all INFO messages
                    format='%(asctime)s - %(levelname)s - %(message)s')

FILE_PATH = '/home/ameer/img-camera-matching/data-base/results/gaussian.json'
PNU_ID_PATH = "pnu_id_path"
BASE_PATH_HIGHEST = "basePathHighest"
BASE_PATH_SECOND_HIGHEST = "basePathsecondHighest"
HIGHEST_CORRELATION_RESULTS = "highest_correlation_results"
SECOND_HIGHEST_CORRELATION_RESULTS = "second_highest_correlation_results"


if __name__ == '__main__':
    logging.info('Entering main function...')
    # Example for camera matching logic
    # args = CameraImageMatcher.parse_arguments()
    # matcher = CameraImageMatcher(args)
    # matcher.run()
    logging.info("Loading all gaussian's pairs")
    allgaussianPairs = LoadAllPairsOfGaussian()
    for x in range(6) :
        logging.info("Loading gaussian's pair")
        g = LoadGaussianPair(**allgaussianPairs.get_gaussian(x))
        path = GAUSSIANPLOTSTHEORY + '_'.join(g.axis_1.split('/')[-1:])+'$'+'_'.join(g.axis_2.split('/')[-1:])
        g.find_gaussian_intersections()
        g.visualize()
    