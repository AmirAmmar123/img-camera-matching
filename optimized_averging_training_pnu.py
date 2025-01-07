import os
import json
from waveLetTransform import WVT
from imgReader import ImgReader
from correlation import correlation
from mylogger import Logger 

class PNUMatcher:
    def __init__(self, base_directory: str, data_dump: str, logger:Logger):
        
        self.base_directory = base_directory
        self.data_dump = data_dump
        self.pnu_img_reader_list = self._get_img_readers('pnu_id')
        self.test_img_reader_list = self._get_img_readers('testing')
        self.correlation_avergin_result = self._load_existing_results()
        self.logger = logger

    def _find_directories(self, directory_name: str) -> list[str]:
        """
        This function walks through the base directory and its subdirectories,
        identifying directories containing the specified directory name.
        """
        return [os.path.join(root, directory_name) for root, dirs, _ in os.walk(self.base_directory) if directory_name in dirs]

    def _get_img_readers(self, directory_name: str) -> list[ImgReader]:
        """
        This function returns a list of ImgReader objects for directories
        that match the specified directory name and have non-zero collections.
        """
        directories = self._find_directories(directory_name)
        return [ImgReader(dir) for dir in directories if ImgReader(dir).get_collection_size() != 0]

    def _load_existing_results(self) -> dict:
        """
        This function loads existing results from the JSON file if it exists.
        """
        if os.path.exists(f'{self.data_dump}data.json'):
            with open(f'{self.data_dump}data.json', 'r') as file:
                return json.load(file)
        return {}

    def calculate_correlation(self):
        """
        This function calculates the average correlation between images in the 'pnu_id'
        directories and the 'testing' directories, storing the results in a dictionary.
        """
        try:
            for pnu_id_reader in self.pnu_img_reader_list:
                pnu_id = pnu_id_reader.get_image_data(0, 'tiff')
                for test_img_reader in self.test_img_reader_list:
                    test_path = test_img_reader.getSetImagePath()
                    pnu_path = pnu_id_reader.getSetImagePath()

                    if test_path not in self.correlation_avergin_result:
                        self.correlation_avergin_result[test_path] = {}

                    if pnu_path in self.correlation_avergin_result[test_path]:
                        # Skip calculation if result already exists
                        self.logger.info(f"Skipping calculation for {test_path} and {pnu_path}")
                        continue

                    self.correlation_avergin_result[test_path][pnu_path] = 0

                    for i in range(test_img_reader.get_collection_size()):
                        try:
                            test_img = test_img_reader.get_image_data(i)
                            result = correlation(pnu_id, WVT(test_img).get_HH())
                            self.correlation_avergin_result[test_path][pnu_path] += result
                        except Exception as e:
                            self.logger.ERROR(f"Exception occurred while processing image {test_img_reader.read_image_path(i)} in {test_path}: {e}")

                    self.correlation_avergin_result[test_path][pnu_path] /= test_img_reader.get_collection_size()
        except Exception as e:
            self.logger.ERROR(f"Exception occurred: {e}")

    def save_results(self):
        """
        This function saves the correlation results to a JSON file.
        It creates the file and its directory if they do not exist.
        """
        
        # File path
        file_path = f'{self.data_dump}data.json'
        
        # Save the results to the file
        with open(file_path, 'w') as file:
            json.dump(self.correlation_avergin_result, file, indent=4)
            self.logger.debug(f'Data successfully saved at {file_path}')

# Usage
if __name__ == "__main__":
    BASE_DIRECTORY = '/home/ameer/img-camera-matching/Data-Base'
    DATA_DUMP = '/home/ameer/img-camera-matching/Data-Base/results/'

    matcher = PNUMatcher(BASE_DIRECTORY, DATA_DUMP)
    matcher.calculate_correlation()
    matcher.save_results()
