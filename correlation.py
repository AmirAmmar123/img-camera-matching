import numpy as np 
from joinData import AllData
from imgReader import ImgReader as ir 
from const import *
import logging 
from waveLetTransform import WVT
import json 
import os 
from const import PNUIDS

logging.basicConfig(level=logging.INFO,  # Set level to INFO to capture all INFO messages
                    format='%(asctime)s - %(levelname)s - %(message)s')

def correlation(pnu_x: np.array,n: np.array):
    """
    Calculates the correlation between two arrays based on the formula: 
    np.dot(n - n^, pnu_x - pnu_x^) / (norm(n - n^) * norm(pnu_x - pnu_x^)). 
    Where:
    - n is the wave-transform F(n).
    - n^ is the average of the image, obtained by applying the inverse wave-transform to F(n).
    - pnu_x is the pnu_id of the set x.
    - pnu_x^ is the average of pnu_id values in the set x.

    Returns the correlation value between the two arrays.

    np.dot(n-n^, pnu_x - pnu_x^) /( norm(n-n^) * norm(pnu_x - pnu_x^) ) 
    n  = the F(n), F is wave-transform 
    n^ = the average( image ),   image=F**-1( F(n) ) 
    pnu_x = pnu_id of the set x 
    pnu_x^ = average of (pnu_id)
    """
    n_gag = np.average(n)
    pnu_x_gag = np.average(pnu_x)
    flat_image1 = (n - n_gag).flatten()
    flat_image2 = (pnu_x - pnu_x_gag).flatten()
    return np.corrcoef(flat_image1, flat_image2)[0,1] 





class CartesianCorrelation:
    def __init__(self, data_set: dict) -> None:
        self.data_set = data_set
        

    def run(self):
        wave_let_transform_mapper = {}
        pnu_ids = {k: ir(k) for k in PNUIDS}

        logging.info("Processing wavelet transform mapper...")

        for set_k in self.data_set.keys():
            wave_let_transform_mapper[set_k] = {}
            for id_key in pnu_ids:
                id = pnu_ids[id_key].get_image_data(0, 'tiff')
                for img_reader in self.data_set[set_k]:
                    if id_key not in wave_let_transform_mapper[set_k]:
                        wave_let_transform_mapper[set_k][id_key] = []
                    for i in range(img_reader.get_collection_size()):
                        try:
                            img = img_reader.get_image_data(i)
                            logging.info(f"Reading image {img_reader.read_image_path(i)}")
                            if img_reader is not None:
                                hh = WVT(img).get_HH()
                                correlation_result = correlation(id, hh)
                                wave_let_transform_mapper[set_k][id_key].append(
                                    self.convert_to_serializable(correlation_result)
                                )
                            else:
                                logging.info('Failed to read image')
                        except Exception as e:
                            logging.error(f"Error processing image {img_reader.read_image_path(i)}: {e}")

            # After processing the current set, save it incrementally
            try:
                save_incremental_data(
                    f'{set_k}.json', {set_k: wave_let_transform_mapper[set_k]}
                )
                logging.info(f"Processed and saved set {set_k}.")
            except Exception as e:
                logging.error(f"Error saving data for set {set_k}: {e}")

        logging.info("Processing complete.")
    def convert_to_serializable(self, data):
        """ Recursively convert wave_let_transform_mapper to be JSON serializable """
        if isinstance(data, dict):
            return {k: self.convert_to_serializable(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.convert_to_serializable(i) for i in data]
        elif isinstance(data, np.ndarray):
            return data.tolist()  # Convert NumPy arrays to lists
        elif isinstance(data, (np.float64, np.float32, np.int64)):
            return float(data)  # Convert NumPy types to native float
        elif isinstance(data, (float, int)):
            return data  # Native numeric types are fine
        else:
            return str(data)  # Convert anything else to string



def save_incremental_data(filename, data):
    """
    Save data incrementally to a JSON file.
    """
    if os.path.exists(filename):
        # Open file, read current contents, and append new data to the list
        with open(filename, 'r+') as f:
            f.seek(0, os.SEEK_END)
            # If not empty, move back one step and add a comma to append new data
            if f.tell() > 0:
                f.seek(f.tell() - 1, os.SEEK_SET)
                f.truncate()
                f.write(",\n")
            json.dump(data, f, indent=4)
            f.write("\n]")  # Close the array
    else:
        # Create new file and write data in an array
        with open(filename, 'w') as f:
            f.write("[\n")
            json.dump(data, f, indent=4)
            f.write("\n]")
