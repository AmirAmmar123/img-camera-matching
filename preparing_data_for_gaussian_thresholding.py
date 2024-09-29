import json
import logging 
logging.basicConfig(level=logging.INFO,  # Set level to INFO to capture all INFO messages
                    format='%(asctime)s - %(levelname)s - %(message)s')
class PreProcessorToThreshold:
    """
    A class to pre-process JSON data for threshold.

    Attributes:
        read_path (str): Path to the input JSON file.  (contains the correlation between each pnu_id and the testing data set)
        write_path (str): Path to the output JSON file. (where to write the most two highest results for each set of correlation)
    """

    def __init__(self, read_path: str, write_path: str):
        """
        Initializes PreProcessorToThreshold with input and output file paths.
        One stage before finding the threshold for each camera.
        
        Args:
            read_path (str): Path to the JSON file to read. (contains the correlation between each pnu_id and the testing data set)
            write_path (str): Path to the JSON file to write. (where to write the most two highest results for each set of correlation)
        """
        self.read_path = read_path
        self.write_path = write_path

    def load_data(self) -> dict:
        """
        Loads data from the JSON file specified by the read path.
        
        Returns:
            dict: The JSON data.
        """
        logging.info(f'loading the json data from {self.read_path}')
        with open(self.read_path, 'r') as file:
            return json.load(file)

    def process_data(self, data: dict) -> dict:
        """
        Processes the loaded data by sorting and filtering.
        
        Args:
            data (dict): The JSON data.
        
        Returns:
            dict: The filtered and sorted data.
        """
        res = {}
        logging.info('Creating a map between the image testing set and the closest two results from the PNU ID')
        for test_set, comparisons in data.items():
            comparisons_relevant = dict(comparisons.items())
            comparisons_relevant_sorted = list(sorted(comparisons_relevant.items(), key=lambda item: item[1]))
            res[test_set.lower()] = comparisons_relevant_sorted

        return {k: {s[0]: s[1] for s in v[-2:]} for k, v in res.items()}

    def save_data(self, data: dict) -> None:
        """
        Saves the processed data to the JSON file specified by the write path.
        
        Args:
            data (dict): The data to write.
        """
        with open(self.write_path, 'w') as file:
            logging.info(f'Saving the result to {self.write_path}')
            json.dump(data, file, indent=4)  

    def run(self) -> None:
        """
        Executes the data processing workflow: load, process, and save data.
        """
        data = self.load_data()
        processed_data = self.process_data(data)
        self.save_data(processed_data)


# Usage
if __name__ == "__main__":
    read_path = "data-base/results/data.json"
    write_path = "data-base/results/preparing_to_thresholding.json"
    processor = PreProcessorToThreshold(read_path, write_path)
    processor.run()
