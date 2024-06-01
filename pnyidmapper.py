import waveLetTransform as wv 
import dataBase as db 
import imgReader as ir 

class Mapper:
    def __init__(self, index: int):
        self.DataBase =  db.DataBase('./Data-Base')
        self.imgReader = ir.ImgReader(self.DataBase.db_index_path(index))
        self.all_transformation = []
        self.all_HH_normalized = []
        self.id = None 
        
    
    def transform_all_imges(self):
        # later change it to self.imgReader.get_collection_size()
        for i in range(10):
            self.all_transformation.append(wv.WVT( self.imgReader.get_image_data(i)))
        return self
    

    def normalized(self): 
        if self.all_transformation:
            for wv in self.all_transformation:
                self.all_HH_normalized.append(wv.get_HH()/self.imgReader.get_collection_size())
            return self
        

    def create_ID(self):
        self.id = sum(self.all_HH_normalized)
        return self.id 
        
if __name__ == "__main__":
    mp = Mapper(2)
    id =  mp.transform_all_imges().normalized().create_ID()
    print(id)
        
        