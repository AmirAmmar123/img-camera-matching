from joinData import AllData 
from imgReader import ImgReader as ir 
from correlation import correlation
from waveLetTransform import WVT 
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
            
    
    def create_two_gussians(self):
        pnu_id = self.pnu_img_reader.get_image_data(0, 'tiff')
        self.highest_correlation_results = []
        self.second_highest_correlation_results = []
        
        for highest_testing_training in self.img_reader_testing_training_Highest:
            for imge_index in range(highest_testing_training.get_collection_size()):
                img = highest_testing_training.get_image_data(imge_index)
                self.highest_correlation_results.append(correlation(pnu_id,WVT(img).get_HH()))
                
        for second_highest_testing_training in self.img_reader_testing_training_Second_Highest:
            for imge_index in range(second_highest_testing_training.get_collection_size()):
                img = second_highest_testing_training.get_image_data(imge_index)
                self.second_highest_correlation_results.append(correlation(pnu_id,WVT(img).get_HH()))
    def print_results(self):
        print(self.highest_correlation_results)
        print(self.second_highest_correlation_results)
if __name__ == "__main__":
    pass 