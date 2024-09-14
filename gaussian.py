from joinData import AllData 
from imgReader import ImgReader as ir 
from correlation import correlation
from waveLetTransform import WVT 
from const import * 
from typing import List, Any
import logging
import time 
import sys 
logging.basicConfig(level=logging.INFO,  # Set level to INFO to capture all INFO messages
                    format='%(asctime)s - %(levelname)s - %(message)s')
class TwoGaussian:
    
    def __init__(self, pnu_id_path_highest: str, basePathHighest:str, basePathsecondHighest:str):
        self.mean = [] 
        self.covariance = []
        self.pnu_id_path = pnu_id_path_highest
        self.basePathHighest = basePathHighest
        self.basePathsecondHighest = basePathsecondHighest
    
    def init_data(self, allData: AllData):
        self.pnu_img_reader = ir(self.pnu_id_path)
        self.img_reader_testing_training_Highest = []
        self.img_reader_testing_training_Second_Highest = []
        for x in range(2):
            self.img_reader_testing_training_Highest.append(
                allData.get_img_reader_by_key(
                    self.basePathHighest + OPTIONS[x]
                )
            )
            self.img_reader_testing_training_Second_Highest.append(
                allData.get_img_reader_by_key(
                    self.basePathsecondHighest + OPTIONS[x]
                )
            )
    
    def create_two_gussians(self):
        pnu_id = self.pnu_img_reader.get_image_data(0, 'tiff')
        self.highest_correlation_results = []
        self.second_highest_correlation_results = []

        start_time = time.time()

        logging.info('Creating first Gaussian...')
        highest_total_images = sum(t.get_collection_size() for t in self.img_reader_testing_training_Highest)
        processed_images = 0
        logging.info(f'{highest_total_images} images ready to be processed...')
        for highest_testing_training in self.img_reader_testing_training_Highest:
            for image_index in range(highest_testing_training.get_collection_size()):
                img = highest_testing_training.get_image_data(image_index)
                self.highest_correlation_results.append(correlation(pnu_id, WVT(img).get_HH()))
                processed_images += 1
                # Print in the same line without creating a new line
                sys.stdout.write(f'\rProcessed {int((processed_images/highest_total_images)*100)}% images.')
                sys.stdout.flush()
        print()
        logging.info(f'Total correlation results for the first Gaussian: {len(self.highest_correlation_results)}')

        logging.info('Finished creating the first Gaussian.')
        logging.info('Creating second Gaussian...')

        second_total_images = sum(t.get_collection_size() for t in self.img_reader_testing_training_Second_Highest)
        processed_images = 0
        logging.info(f'{second_total_images} images ready to be processed...')
        for second_highest_testing_training in self.img_reader_testing_training_Second_Highest:
            for image_index in range(second_highest_testing_training.get_collection_size()):
                img = second_highest_testing_training.get_image_data(image_index)
                self.second_highest_correlation_results.append(correlation(pnu_id, WVT(img).get_HH()))

                processed_images += 1
                # Print in the same line without creating a new line
                sys.stdout.write(f'\rProcessed {int((processed_images/second_total_images)*100)}% images.')
                sys.stdout.flush()
          
        print()
        logging.info(f'Total correlation results for the second Gaussian: {len(self.second_highest_correlation_results)}')

        total_processed = len(self.highest_correlation_results) + len(self.second_highest_correlation_results)
        elapsed_time = time.time() - start_time
        total_images = highest_total_images + second_total_images
        logging.info('Finished processing.')
        logging.info(f'Total images : {total_images}')
        logging.info(f'Total correlation results: {total_processed}')
        logging.info(f'Time elapsed: {elapsed_time:.2f} seconds')

    
    def get_results(self):
        return {
            'pnu_id_path': self.pnu_id_path,
            'basePathHighest': self.basePathHighest,
            'basePathsecondHighest': self.basePathsecondHighest,
            'highest_correlation_results': self.highest_correlation_results,
            'second_highest_correlation_results': self.second_highest_correlation_results
        }
