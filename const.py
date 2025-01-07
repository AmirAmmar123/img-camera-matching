import os 

HOME = os.path.expanduser("~") 
PROJECT_DIR = 'img-camera-matching'
DB = 'data-base'
RESULT = 'results'
TRAINING = "/training/"
TESTING = "/testing/"
PNU_DIR = 'pnu_id'
LOGGER_DIR = 'logging'
LOGGER_FILE ='logger'

PROJECT_PATH =f'{HOME}/{PROJECT_DIR}'
DATABASE_PATH =  f'{HOME}/{PROJECT_DIR}/{DB}'
NUMS_OF_DATAT_SET = len([name for name in os.listdir(f'{HOME}/{PROJECT_DIR}/{DB}') if os.path.isdir(os.path.join(f'{HOME}/{PROJECT_DIR}/{DB}', name)) and name != RESULT])


RESULTS  = f'{DATABASE_PATH}/{RESULT}'

OPTIONS = [TRAINING, TESTING]
GAUSSIANPLOTS= './plots/gaussian/'
GAUSSIANPLOTSTHEORY = f'{GAUSSIANPLOTS}theoretical/'


PNUIDS = [
    f'{DATABASE_PATH}/{name}/{PNU_DIR}/' for name in os.listdir(DATABASE_PATH) 
    if os.path.isdir(os.path.join(DATABASE_PATH, name)) and name != RESULT
]

JSON_FILES = [
        f'{DATABASE_PATH}/{name}.json' for name in os.listdir(DATABASE_PATH) 
    if os.path.isdir(os.path.join(DATABASE_PATH, name)) and name != RESULT
]


THRESHOLDS = [0.0009 ,0.001, 0.0019, 0.002, 0.00245, 0.003] 


