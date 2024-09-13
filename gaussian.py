from joinData import AllData 
from imgReader import ImgReader as ir 
from correlation import correlation
from waveLetTransform import WVT 
from const import * 

class TwoGaussian:
    
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
        print('Creating highest correlation')
        for highest_testing_training in self.img_reader_testing_training_Highest:
            for imge_index in range(highest_testing_training.get_collection_size()):
                img = highest_testing_training.get_image_data(imge_index)
                self.highest_correlation_results.append(correlation(pnu_id,WVT(img).get_HH()))
        print('Finished')
        print('Creating Second highest correlation')
        for second_highest_testing_training in self.img_reader_testing_training_Second_Highest:
            for imge_index in range(second_highest_testing_training.get_collection_size()):
                img = second_highest_testing_training.get_image_data(imge_index)
                self.second_highest_correlation_results.append(correlation(pnu_id,WVT(img).get_HH()))
        print('Finished')
    def stage_for_json(self):
        self.results = [
            self.pnu_id_path,
            self.basePathHighest,
            self.basePathsecondHighest,
            self.highest_correlation_results,
            self.second_highest_correlation_results
        ]
    
    def get_results(self):
        return self.results

