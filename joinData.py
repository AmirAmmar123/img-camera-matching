from waveLetTransform import WVT
from dataBase import DataBase as db 
from imgReader import ImgReader as ir 
from const import *
import logging 
logging.basicConfig(level=logging.INFO,  # Set level to INFO to capture all INFO messages
                    format='%(asctime)s - %(levelname)s - %(message)s')
class AllData:
    TRAINING = "training"
    TESTING = "testing"

    def __init__(self, dataBasePath):
        """
        Initialize an instance of AllData class.
        Pre-process stage, that joins both training and testing images as one set.

        Parameters:
        dataBasePath (str): The path to the database directory.
        """
        logging.info('Initializing Data in ALLDATA...')
        self.dataBaseTesting =  db(dataBasePath, self.TRAINING)
        self.dataBaseTraining=  db(dataBasePath, self.TESTING)
        self.all_data = None
        self.imagReaderMapped = {}
        logging.info('Data successfully initialized')
    def join(self,):
        """
        Joins both training and testing dataset paths into one list.
        """
        logging.info('Joing training and testing images')
        self.all_data = [
            HOME_DIR_PATH+self.dataBaseTraining.imgDirIndexPath(i) for i in range(NUMS_OF_DATAT_SET)
        ] + [
            HOME_DIR_PATH+self.dataBaseTesting.imgDirIndexPath(i) for i in range(NUMS_OF_DATAT_SET)

        ]


    def map_to_imges(self):
        """
        Maps image paths to ImgReader instances.
        """
        for path_to_im in self.all_data:
            self.imagReaderMapped[path_to_im] = ir(path_to_im)

    def get_img_reader_by_key(self, key):
        """
        Returns the ImgReader instance for a given image path key.
        """
        return self.imagReaderMapped[key]
    
if __name__ == "__main__":
    all_data = AllData(DATABASE_PATH)
    all_data.join()
    all_data.map_to_imges()
    print(all_data)
    