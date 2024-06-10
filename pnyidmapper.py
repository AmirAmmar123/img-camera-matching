import waveLetTransform as wv 
import dataBase as db 
import imgReader as ir 
import numpy as np
import os 
import cv2 

class Mapper:
    IDS_DIRECTORY_PATH = './Data-Base/PNU-IDs/'
    def __init__(self, index: int):
        self.DataBase =  db.DataBase('./Data-Base')
        self.imgReader = ir.ImgReader(self.DataBase.db_index_path(index)) # The data-specific-data-set-path-inside image reader
        self.all_transformation = []
        self.all_HH_normalized = []
        self.id = None 
        self.std = None 
        self.mean = None 
        self.min = None 
        self.max = None 
    
    def transform_all_imges(self):
        """Transform all images within the set of images"""
        # for i in range(self.imgReader.get_collection_size()):
        for i in range(1):
            self.all_transformation.append(wv.WVT( self.imgReader.get_image_data(i)))
        return self
    

    def create_ID(self):
        self.id = sum([wvt.get_HH() for wvt in self.all_transformation ])/self.imgReader.get_collection_size() 
        self.max, self.min, self.mean, self.std = np.max(self.id), np.min(self.id), np.mean(self.id), np.var(self.id)**0.5
        return self

    def saveID(self):
        # still not finished 
        base_name = os.path.basename(self.imgReader.getSetImagePath())
        cv2.imwrite(self.IDS_DIRECTORY_PATH+base_name+'.jpg', self.id)

             
if __name__ == "__main__":
    mp = Mapper(2)
    id =  mp.transform_all_imges().create_ID().saveID()
                