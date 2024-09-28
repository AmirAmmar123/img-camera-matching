# sourcery skip: avoid-builtin-shadow
from cameraImageMatcher import CameraImageMatcher
from loadGussian import LoadAllPairsOfGaussian, LoadGaussianPair
from const import GAUSSIANPLOTSTHEORY
from matplotlib import pyplot as plt
import logging
from joinData import AllData
from waveLetTransform import WVT
from correlation import correlation
from imgReader import ImgReader as ir
from const import * 
import json
import numpy as np

logging.basicConfig(level=logging.INFO,  # Set level to INFO to capture all INFO messages
                    format='%(asctime)s - %(levelname)s - %(message)s')

def convert_to_serializable(data):
    """ Recursively convert wave_let_transform_mapper to be JSON serializable """
    if isinstance(data, dict):
        return {k: convert_to_serializable(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_to_serializable(i) for i in data]
    elif isinstance(data, np.ndarray):
        return data.tolist()  # Convert NumPy arrays to lists
    elif isinstance(data, (np.float64, np.float32, np.int64)):
        return float(data)  # Convert NumPy types to native float
    elif isinstance(data, (float, int)):
        return data  # Native numeric types are fine
    else:
        return str(data)  # Convert anything else to string

if __name__ == '__main__':
    logging.info('Entering main function...')
    
    # Example for camera matching logic
    matcher = CameraImageMatcher(CameraImageMatcher.parse_arguments())
    logging.info("CameraImageMatcher initialized successfully.")

    # Uncomment to run matcher logic
    # matcher.run()
    
    # logging.info("Loading all gaussian's pairs")
    # allgaussianPairs = LoadAllPairsOfGaussian()
    # for x in range(6):
    #     logging.info("Loading gaussian's pair")
    #     g = LoadGaussianPair(**allgaussianPairs.get_gaussian(x))
    #     path = GAUSSIANPLOTSTHEORY + '_'.join(g.axis_1.split('/')[-1:])+'$'+'_'.join(g.axis_2.split('/')[-1:])
    #     g.find_gaussian_intersections()
    #     g.visualize(path)

    alldata = AllData(matcher.db_bath)
    logging.info("Joining all data...")
    alldata.join()
    alldata.map_to_imges()
    data_set = alldata.join_training_and_testig_as_one_dir()
    logging.info("Data joined and prepared.")

    wave_let_transform_mapper = {}
    pnu_ids = {k: ir(k) for k in PNUIDs}

    logging.info("Processing wavelet transform mapper...")
    for set_k in data_set.keys():
        wave_let_transform_mapper[set_k] = {}
        for id_key in pnu_ids:
            id = pnu_ids[id_key].get_image_data(0, 'tiff')
            for img_reader in data_set[set_k]:
                if id_key not in wave_let_transform_mapper[set_k]:
                    wave_let_transform_mapper[set_k][id_key] = []
                for i in range(img_reader.get_collection_size()):
                    img = img_reader.get_image_data(i)
                    logging.info(f"Reading image {img_reader.read_image_path(i)}")
                    correlation_result = correlation(id, WVT(img).get_HH())
                    wave_let_transform_mapper[set_k][id_key].append(
                        convert_to_serializable(correlation_result)
                    )
        logging.info(f"Processed set {set_k}.")

    # Convert the entire mapper to a serializable form
    serializable_data = convert_to_serializable(wave_let_transform_mapper)
    logging.info("Converted wave_let_transform_mapper to a serializable format.")

    # Save to JSON
    with open('wave_let_transform_mapper.json', 'w') as f:
        json.dump(serializable_data, f, indent=4)
        logging.info("Data saved to wave_let_transform_mapper.json")

    logging.info("Processing complete.")
