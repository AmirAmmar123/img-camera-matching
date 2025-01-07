from dataBase import DataBase as db 
from imgReader import ImgReader as ir 
from const import *
from mylogger import Logger
class AllData:
    TRAINING = "training"
    TESTING = "testing"

    def __init__(self, dataBasePath,  logger:Logger):
        """
        Initialize an instance of AllData class.
        Pre-process stage, that joins both training and testing images as one set.

        Parameters:
        dataBasePath (str): The path to the database directory.
        """
        self.dataBaseTesting =  db(dataBasePath,logger, self.TESTING)
        self.dataBaseTraining=  db(dataBasePath,logger,self.TRAINING)
        self.all_data = None
        self.imagReaderMapped = {}
        self.logger =  logger
    def join(self,):
        """
        Joins both training and testing dataset paths into one list.
        """
        self.logger.info('Joing training and testing images')
        self.all_data = [
            self.dataBaseTraining.imgDirIndexPath(i) for i in range(NUMS_OF_DATAT_SET)
        ] + [
            self.dataBaseTesting.imgDirIndexPath(i) for i in range(NUMS_OF_DATAT_SET)

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

    
    def join_training_and_testig_as_one_dir(self):
        mapper = {}
        for path in self.all_data:
            key = '/'.join(path.split('/')[:-2])
            if key not in mapper:
                mapper[key] = []
            mapper[key].append(self.get_img_reader_by_key(path))
        return mapper
if __name__ == "__main__":
    all_data = AllData(DATABASE_PATH)
    all_data.join()
    all_data.map_to_imges()
    print(all_data)
    