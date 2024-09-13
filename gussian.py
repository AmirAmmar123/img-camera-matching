from joinData import AllData 
from imgReader import ImgReader as ir 
import json
import os 

NUMS_OF_DATAT_SET = 6 
NUM_OF_GUSSIANS = NUMS_OF_DATAT_SET 
DATABASE_PATH = "data-base"
TRAINING = "/training/"
TESTING = "/testing/"
OPTIONS = [TRAINING, TESTING]
PNU = "/pnu_id/"
PNU_IMG_NAME = "pnu_id.tiff"

class TwoGussian:
    
    def __init__(self, pnu_id_path_highest: str, basePathHighest:str, basePathsecondHighest:str):
        self.mean= [] 
        self.covariance = []
        self.pnu_id_path = pnu_id_path_highest
        self.basePathHighest = basePathHighest
        self.basePathsecondHighest = basePathsecondHighest
        
    
    def init_data(self, allData : AllData ):
        self.pnu_img_reader = ir(self.pnu_id_path)
        self.img_reader_testing_training_Highest = []
        self.img_reader_testing_training_Second_Highest = []
        for x in range(2):
            self.img_reader_testing_training_Highest.append(
                allData.get_img_reader_by_key(self.basePathHighest + OPTIONS[x])
            )
            self.img_reader_testing_training_Second_Highest.append(
                self.basePathsecondHighest + OPTIONS[x]
                )
            
       

if __name__ == "__main__":
    pass 