# sourcery skip: avoid-builtin-shadow
from cameraImageMatcher import CameraImageMatcher
from loadGussian import LoadAllPairsOfGaussian, LoadGaussianPair
from const import GAUSSIANPLOTSTHEORY
from joinData import AllData
from correlation import CartesianCorrelation
from const import * 
from load_final_data import JSONDataPlotter, JSONDataProcessor
from mylogger import Logger
import datetime
import os
import argparse

parser = argparse.ArgumentParser(description="Image Camera Matcher")
parser.add_argument("--db_path", type=str, default=f'{DATABASE_PATH}', help="Path to the Data-Base")
parser.add_argument("--data_dump", type=str, default=f'{DATABASE_PATH}/results/', help="Path to Dump the output results")
parser.add_argument("--home_directory_path", type=str, default=f'{HOME}/', help="Home directory path")
parser.add_argument("--read_correlation_result", type=str, default=f'{DATABASE_PATH}/results/data.json', help="The correlation result between the data-base and the PNU ID will be saved here")
parser.add_argument("--save_to_gaussian_stage", type=str, default=f'{DATABASE_PATH}/results/prep_to_threshold.json', help="Closest points between the data-base and PNU ID will be saved here")
parser.add_argument("--save_to_gaussian", type=str, default=f'{DATABASE_PATH}/results/gaussian.json', help="Save the Gaussian results to this directory")
parser.add_argument("--load_gaussian", type=str, default=f'{DATABASE_PATH}/results/gaussian.json',help='Load the pairs of gaussian the have been created')
parser.add_argument("--create_x_pnu_id", type=int, default=0, help="Number of PNU IDs to create")
parser.add_argument("--activate_creation", type=bool, default=False, help="Activate the generation of PNU ID for each image data set")
parser.add_argument("--activate_matcher", type=bool, default=False, help="Activate the correlation generation between image-set and PNU ID")
args = parser.parse_args()
os.environ['LOGGER'] = f'{LOGGER_DIR}/{LOGGER_FILE}_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log'

if __name__ == '__main__':
    main_logger = Logger(f'Message:', os.environ['LOGGER'])
    main_logger.info('Entering main function...')
    main_logger.debug(f'Args passed: { vars(args)}')
    matcher = CameraImageMatcher(args, main_logger)
    main_logger.info("CameraImageMatcher initialized successfully.")
    matcher.run()
    main_logger.info("Loading all gaussian's pairs")
    
    
    allgaussianPairs = LoadAllPairsOfGaussian()
    for x in range(NUMS_OF_DATAT_SET):
        main_logger.info("Loading gaussian's pair")
        g = LoadGaussianPair( main_logger,**allgaussianPairs.get_gaussian(x))
        path = GAUSSIANPLOTSTHEORY + '_'.join(g.axis_1.split('/')[-1:])+'$'+'_'.join(g.axis_2.split('/')[-1:])
        g.visualize(path)

    alldata = AllData(matcher.db_path, main_logger)
    main_logger.info("Joining all data...")
    alldata.join()
    alldata.map_to_imges()
    data_set = alldata.join_training_and_testig_as_one_dir()
    main_logger.info("Data joined and prepared.")
    CartesianCorrelation(data_set, main_logger).run()
    processor = JSONDataProcessor()
    processor.process_json_files()
    JSONDataPlotter(f'{PROJECT_PATH}/pnuid_results.xlsx').plot_all()
    