# sourcery skip: avoid-builtin-shadow
from cameraImageMatcher import CameraImageMatcher
from loadGussian import LoadAllPairsOfGaussian, LoadGaussianPair
from const import GAUSSIANPLOTSTHEORY
from matplotlib import pyplot as plt
import logging
from joinData import AllData
from waveLetTransform import WVT
from correlation import correlation, CartesianCorrelation
from imgReader import ImgReader as ir
from const import * 
import json
import numpy as np
import os 


logging.basicConfig(level=logging.INFO,  # Set level to INFO to capture all INFO messages
                    format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    logging.info('Entering main function...')

   
    matcher = CameraImageMatcher(CameraImageMatcher.parse_arguments())
    logging.info("CameraImageMatcher initialized successfully.")

    matcher.run()

    logging.info("Loading all gaussian's pairs")
    allgaussianPairs = LoadAllPairsOfGaussian()
    for x in range(6):
        logging.info("Loading gaussian's pair")
        g = LoadGaussianPair(**allgaussianPairs.get_gaussian(x))
        path = GAUSSIANPLOTSTHEORY + '_'.join(g.axis_1.split('/')[-1:])+'$'+'_'.join(g.axis_2.split('/')[-1:])
        g.find_gaussian_intersections()
        g.visualize(path)

    alldata = AllData(matcher.db_bath)
    logging.info("Joining all data...")
    alldata.join()
    alldata.map_to_imges()
    data_set = alldata.join_training_and_testig_as_one_dir()
    logging.info("Data joined and prepared.")
    CartesianCorrelation(data_set).run()