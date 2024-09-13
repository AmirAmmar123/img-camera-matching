import json
import os

class DataProcessor:
    """
    A class to process JSON data for thresholding.

    Attributes:
        read_path (str): Path to the input JSON file.
        write_path (str): Path to the output JSON file.
    """

    def __init__(self, read_path: str, write_path: str):
        """
        Initializes DataProcessor with input and output file paths.
        
        Args:
            read_path (str): Path to the JSON file to read.
            write_path (str): Path to the JSON file to write.
        """
        self.read_path = read_path
        self.write_path = write_path

    def load_data(self) -> dict:
        """
        Loads data from the JSON file specified by the read path.
        
        Returns:
            dict: The JSON data.
        """
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
        for test_set, comparisons in data.items():
            comparisons_relevant = {k: v for k, v in comparisons.items()}
            comparisons_relevant_sorted = list(sorted(comparisons_relevant.items(), key=lambda item: item[1]))
            res[test_set] = comparisons_relevant_sorted
        
        filtered = {}
        for k, v in res.items():
            filtered[k] = {s[0]: s[1] for s in v[-2:]}
        
        return filtered

    def save_data(self, data: dict) -> None:
        """
        Saves the processed data to the JSON file specified by the write path.
        
        Args:
            data (dict): The data to write.
        """
        with open(self.write_path, 'w') as file:
            json.dump(data, file, indent=4)  # Pretty print with indent

    def run(self) -> None:
        """
        Executes the data processing workflow: load, process, and save data.
        """
        data = self.load_data()
        processed_data = self.process_data(data)
        self.save_data(processed_data)


# Usage
if __name__ == "__main__":
    read_path = "Data-Base/results/data.json"
    write_path = "Data-Base/results/preparing_to_thresholding.json"
    processor = DataProcessor(read_path, write_path)
    processor.run()
