import os 

PROJECT_DIR = 'img-camera-matching'
DB = 'data-base'
RESULT = 'results'
TRAINING = "/training/"
TESTING = "/testing/"
PNU_dir = '/pnu_id/'
PNU_ID_PATH = "pnu_id_path"
BASE_PATH_HIGHEST = "basePathHighest"
BASE_PATH_SECOND_HIGHEST = "basePathsecondHighest"
HIGHEST_CORRELATION_RESULTS = "highest_correlation_results"
SECOND_HIGHEST_CORRELATION_RESULTS = "second_highest_correlation_results"
NUMS_OF_DATAT_SET = NUMS_OF_DATAT_SET = NUM_CAMERAS = 6
NUM_OF_GUSSIANS = NUMS_OF_DATAT_SET
HOME = os.path.expanduser("~") 
FULL_PATH =f'{HOME}/{PROJECT_DIR}'
DATABASE_PATH =  f'{HOME}/{PROJECT_DIR}/{DB}'
CAMERA_SET_ID = list(range(NUM_CAMERAS))
RESULTS  = f'{DATABASE_PATH}/{RESULT}'
READ_RESULTS= f'{RESULTS}data.json'
WRITE_SORTED= f'{RESULTS}preparing_to_thresholding.json'
READ_SORTED = f'{RESULTS}preparing_to_thresholding.json'
ALL_RESULTS_DIR = f'{FULL_PATH}/all_results/'
NUM_OF_GUSSIANS = NUMS_OF_DATAT_SET
OPTIONS = [TRAINING, TESTING]
PATH_TO_GUSSIAN_JSON_FILE = f'{RESULTS}gussians.json'
GAUSSIANPLOTS= './plots/gaussian/'
GAUSSIANPLOTSTHEORY = f'{GAUSSIANPLOTS}theoretical/'
PNU_DIR = 'pnu_id'
PNUIDS = [
    f'{ALL_RESULTS_DIR}iphone-13-pro-amir/{PNU_DIR}',
    f'{ALL_RESULTS_DIR}iphone-14-plus-abeer/{PNU_DIR}',
    f'{ALL_RESULTS_DIR}iphone-8-plus-amir/{PNU_DIR}',
    f'{ALL_RESULTS_DIR}iphone-areeg/{PNU_DIR}',
    f'{ALL_RESULTS_DIR}iphone-hanaa/{PNU_DIR}',
    f'{ALL_RESULTS_DIR}iphone14-pro/{PNU_DIR}'
]

SETS = [
    f'{DATABASE_PATH}/iphone-13-pro-amir',
    f'{DATABASE_PATH}/iphone-14-plus-abeer',
    f'{DATABASE_PATH}/iphone-8-plus-amir',
    f'{DATABASE_PATH}/iphone-areeg',
    f'{DATABASE_PATH}/iphone-hanaa',
    f'{DATABASE_PATH}/iphone14-pro'
]

FILE_PATH = f'{RESULTS}gaussian.json'


JSON_FILES = [
    "iphone14-pro.json",
    "iphone-8-plus-amir.json",
    "iphone-13-pro-amir.json",
    "iphone-14-plus-abeer.json",
    "iphone-areeg.json",
    "iphone-hanaa.json"
]
