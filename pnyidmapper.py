from typing import Any, Generator
from waveLetTransform import WVT 
import dataBase as db 
import imgReader as ir 
import numpy as np
import cv2 
from functools import reduce

class Mapper:

    def __init__(self,dataBasePath: str, directoryIndex: int):
        self.DataBase =  db.DataBase(dataBasePath)
        self.imgReader = ir.ImgReader(self.DataBase.db_index_path(directoryIndex)) # The data-specific-data-set-path-inside image reader
        self.all_transformation = []
        self.all_HH_normalized = []
        self.id = None 
        self.std = None 
        self.mean = None 
        self.min = None 
        self.max = None 
    
    def transform_all_imges(self) -> Generator[Any, Any, Any]:
        """Transform all images within the set of images"""
        for i in range(self.imgReader.get_collection_size()):
            yield WVT( self.imgReader.get_image_data(i))
        
    

    def create_ID(self) -> Any:
        """
        Creates an ID image based on the transformed images and calculates statistics.

        Args:
            self: The instance of the class.

        Returns:
            The instance with the ID image and calculated statistics.
        """
        self.id = (
            sum(wvt.get_HH() for wvt in self.transform_all_imges())
            / self.imgReader.get_collection_size()
        )
        self.max, self.min, self.mean, self.std = np.max(self.id), np.min(self.id), np.mean(self.id), np.var(self.id)**0.5
        return self

    def saveID(self)-> None:
        """
        Saves the ID image to a specified path.

        Args:
            self: The instance of the class.

        """
        path = self.imgReader.getSetImagePath().replace('training','pnu_id')
        cv2.imwrite(f'{path}pnu_id.tiff', self.id)


if __name__ == "__main__":
    mp = Mapper('./Data-Base',1)
    mp.transform_all_imges()
    mp.create_ID().saveID()
                