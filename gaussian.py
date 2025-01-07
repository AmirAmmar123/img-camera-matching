from joinData import AllData 
from imgReader import ImgReader as ir 
from correlation import correlation
from waveLetTransform import WVT 
from const import * 
from mylogger import  Logger
import time 
import sys 

class GaussianPairs:
    
    def __init__(self, pnu_id_path_highest: str, basePathHighest:str, basePathsecondHighest:str,  logger:Logger):
        """
        A class to create two Gaussian distributions based on the closest correlation results between 
        a set of images and PNU IDs. The class processes two sets of images to compute correlations 
        with a given PNU ID, and stores the results for further analysis.

        Attributes:
            mean (list): Placeholder for storing the mean of the Gaussians.
            covariance (list): Placeholder for storing the covariance of the Gaussians.
            pnu_id_path (str): Path to the highest PNU ID data.
            basePathHighest (str): Path to the dataset with the highest priority for correlation.
            basePathsecondHighest (str): Path to the dataset with the second highest priority for correlation.
        """
        self.mean = [] 
        self.covariance = []
        self.pnu_id_path = pnu_id_path_highest
        self.basePathHighest = basePathHighest
        self.basePathsecondHighest = basePathsecondHighest
        self.logger =  logger
    
    def init_data(self, allData: AllData):
        """
        Initialize image readers for the datasets and PNU IDs, setting up the data for correlation computation.

        Args:
            allData (AllData): An instance of AllData containing methods to retrieve image readers 
                               for both the highest and second-highest datasets.
        """
        self.pnu_img_reader = ir(self.pnu_id_path)
        self.img_reader_testing_training_Highest = []
        self.img_reader_testing_training_Second_Highest = []
        self.logger.info("Initializing the image reader of both chosen gaussian's pairs")
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

        self.logger.info('Creating first Gaussian...')
        highest_total_images = sum(t.get_collection_size() for t in self.img_reader_testing_training_Highest)
        processed_images = 0
        self.logger.info(f'{highest_total_images} images ready to be processed...')
        for highest_testing_training in self.img_reader_testing_training_Highest:
            for image_index in range(highest_testing_training.get_collection_size()):
                img = highest_testing_training.get_image_data(image_index)
                self.highest_correlation_results.append(correlation(pnu_id, WVT(img).get_HH()))
                processed_images += 1
                # Print in the same line without creating a new line
                sys.stdout.write(f'\rProcessed {int((processed_images/highest_total_images)*100)}% images.')
                sys.stdout.flush()
        print()
        self.logger.debug(f'Total correlation results for the first Gaussian: {len(self.highest_correlation_results)}')

        self.logger.info('Finished creating the first Gaussian.')
        self.logger.info('Creating second Gaussian...')

        second_total_images = sum(t.get_collection_size() for t in self.img_reader_testing_training_Second_Highest)
        processed_images = 0
        self.logger.info(f'{second_total_images} images ready to be processed...')
        for second_highest_testing_training in self.img_reader_testing_training_Second_Highest:
            for image_index in range(second_highest_testing_training.get_collection_size()):
                img = second_highest_testing_training.get_image_data(image_index)
                self.second_highest_correlation_results.append(correlation(pnu_id, WVT(img).get_HH()))

                processed_images += 1
                # Print in the same line without creating a new line
                sys.stdout.write(f'\rProcessed {int((processed_images/second_total_images)*100)}% images.')
                sys.stdout.flush()
          
        print()
        self.logger.debug(f'Total correlation results for the second Gaussian: {len(self.second_highest_correlation_results)}')

        total_processed = len(self.highest_correlation_results) + len(self.second_highest_correlation_results)
        elapsed_time = time.time() - start_time
        total_images = highest_total_images + second_total_images
        self.logger.info('Finished processing.')
        self.logger.info(f'Total images : {total_images}')
        self.logger.info(f'Total correlation results: {total_processed}')
        self.logger.info(f'Time elapsed: {elapsed_time:.2f} seconds')

    
    def get_results(self):
        return {
            'pnu_id_path': self.pnu_id_path,
            'basePathHighest': self.basePathHighest,
            'basePathsecondHighest': self.basePathsecondHighest,
            'highest_correlation_results': self.highest_correlation_results,
            'second_highest_correlation_results': self.second_highest_correlation_results
        }
