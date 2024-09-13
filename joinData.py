from waveLetTransform import WVT
from dataBase import DataBase as db 
from imgReader import ImgReader as ir 
from const import *
class AllData:
    TRAINING = "training"
    TESTING = "testing"

    def __init__(self, dataBasePath):
        """
        Initialize an instance of AllData class.

        Parameters:
        dataBasePath (str): The path to the database directory.

        Attributes:
        dataBaseTesting (db): An instance of the DataBase class for testing data.
        dataBaseTraining (db): An instance of the DataBase class for training data.
        all_data (list): A list to store paths to all images. Initialized as None.
        imagReaderMapped (dict): A dictionary to store image readers mapped by their paths.

        """
        self.dataBaseTesting =  db(dataBasePath, self.TRAINING)
        self.dataBaseTraining=  db(dataBasePath, self.TESTING)
        self.all_data = None
        self.imagReaderMapped = {}
    def join(self,):
        self.all_data = [
            HOME_DIR_PATH+self.dataBaseTraining.imgDirIndexPath(i) for i in range(NUMS_OF_DATAT_SET)
        ] + [
            HOME_DIR_PATH+self.dataBaseTesting.imgDirIndexPath(i) for i in range(NUMS_OF_DATAT_SET)

        ]


    def map_to_imges(self):
        for path_to_im in self.all_data:
            self.imagReaderMapped[path_to_im] = ir(path_to_im)

    def get_img_reader_by_key(self, key):
        return self.imagReaderMapped[key]
    
if __name__ == "__main__":
    all_data = AllData(DATABASE_PATH)
    all_data.join()
    all_data.map_to_imges()
    print(all_data)
    