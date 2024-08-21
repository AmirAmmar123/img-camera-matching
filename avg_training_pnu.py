import os
from waveLetTransform import WVT
from imgReader import ImgReader
from correlation import correlation

BASE_DIRECTORY = '/home/ameer/img-camera-matching/Data-Base'

def find_pnu_id_directories(base_directory):
    return [os.path.join(root, 'pnu_id') for root, dirs, files in os.walk(base_directory) if 'pnu_id' in dirs]

def find_testing_directories(base_directory):
    return [os.path.join(root, 'testing') for root, dirs, files in os.walk(base_directory) if 'testing' in dirs]

pnu_id_dirs = find_pnu_id_directories(BASE_DIRECTORY)
pnu_img_reader_list = [ImgReader(pnu_id_dir) for pnu_id_dir in pnu_id_dirs if ImgReader(pnu_id_dir).get_collection_size() != 0]

test_dirs = find_testing_directories(BASE_DIRECTORY)
test_img_reader_list = [ImgReader(test_dir) for test_dir in test_dirs if ImgReader(test_dir).get_collection_size() != 0]


# TODO: Do a correlation with each pnu_id to all the images in given set (also do transformation to this images), and devide by the size of the set 
# dave the value 
