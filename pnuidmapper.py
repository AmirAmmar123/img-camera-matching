from typing import Any, Generator
from waveLetTransform import WVT 
import dataBase as db 
import imgReader as ir 
import numpy as np
import cv2 
import json
import logging 
import logging 
import os 
logging.basicConfig(level=logging.INFO,  # Set level to INFO to capture all INFO messages
                    format='%(asctime)s - %(levelname)s - %(message)s')
class Mapper:
    MAX = 'max'
    MIN = 'min'
    MEAN = 'mean'
    STD = 'std'
    
    def __init__(self,dataBasePath: str, directoryIndex: int, readfrom : str = 'training' ):
        print('Initializing PNU matcher...')
        self.DataBase =  db.DataBase(dataBasePath, readfrom)
        self.imgReader = ir.ImgReader(self.DataBase.imgDirIndexPath(directoryIndex)) # The data-specific-data-set-path-inside image reader
        self.readfrom = readfrom
        self.all_transformation = []
        self.all_HH_normalized = []
        self.pnu_id = None 
        self.std = None 
        self.mean = None 
        self.min = None 
        self.max = None
        print('PNU matcher successfully initialized')
    
    def transform_all_imges(self) -> Generator[Any, Any, Any]:
        logging.info(f'Casting WaveLetTransform for all images in {self.imgReader.path}...')
        """
            Transform all images within the set of images
        """
        for i in range(self.imgReader.get_collection_size()):
            yield WVT( self.imgReader.get_image_data(i))
        


    def create_ID(self):
        """
        Creates an PNU ID image based on the transformed images and calculates statistics.

        Args:
            self: The instance of the class.

        Returns:
            The instance with the ID image and calculated statistics.
        """
       
        logging.info('Creating PNU ID...')
        self.pnu_id = (
            sum(wvt.get_HH() for wvt in self.transform_all_imges())
            / self.imgReader.get_collection_size()
        )
        self.max, self.min, self.mean, self.std = np.max(self.pnu_id), np.min(self.pnu_id), np.mean(self.pnu_id), np.var(self.pnu_id)**0.5
        return self

    def saveID(self)-> None:
        """
        Saves the ID image to a specified path.

        Args:
            self: The instance of the class.
        """
      
        path = self.imgReader.getSetImagePath().replace(self.readfrom,'pnu_id')
        cv2.imwrite(f'{path}pnu_id.tiff', self.pnu_id)
        
        data = {
        self.MAX: self.max,
        self.MIN: self.min,
        self.MEAN: self.mean,
        self.STD: self.std
                }
     
        with open(f'{path}data.json', 'w') as file:
                json.dump(data, file, indent=4)
  
        logging.info(f'PNU Id and Data successfully saved at {path}')

    def save_transformations(self) -> None:
        """
        Appends transformed images' HH components into a JSON file incrementally,
        without loading all existing data into memory.
        
        Args:
            self: The instance of the class.
        """
        logging.info('Saving transformed images incrementally...')
        
        # Construct the path for the transformations file
        path = self.imgReader.getSetImagePath().replace(self.readfrom, '')
        transformations_file = os.path.join(path, 'transformations.json')

        # Check if the file exists and whether it's empty
        file_exists = os.path.exists(transformations_file)
        append_mode = 'a' if file_exists else 'w'

        # Open the file in append mode
        with open(transformations_file, append_mode) as file:
            if not file_exists:
                # Write the opening bracket for the JSON list if the file doesn't exist
                file.write("[\n")

            # Process each image one by one and append its transformation
            first_item = True if not file_exists else False

            for wvt in self.transform_all_imges():
                hh_component = wvt.get_HH().tolist()  # Get the HH component of the wavelet

                # If the file already has content, add a comma before each new transformation
                if not first_item:
                    file.write(",\n")
                json.dump(hh_component, file, indent=4)
                first_item = False
                logging.info(f'Successfully appended transformation for one image')

            # If it's the last image, close the JSON list correctly
            file.write("\n]")

        logging.info(f'All transformations successfully saved at {transformations_file}')


if __name__ == "__main__":
    DB = './data-base'
    for i in range(6):
        mp = Mapper(DB,i, 'training')
        mp.save_transformations()  # Call this method to save transformation
        mp = Mapper(DB,i, 'testing')
        mp.save_transformations()  # Call this method to save transformation
    # mp.transform_all_imges()
    # mp.create_ID().saveID()