import json
import numpy as np
import os
from const import * 

class JSONDataProcessor:
    def __init__(self, json_files, results_dir, database_path, pnuids, thresholds):
        self.json_files = json_files
        self.results_dir = results_dir
        self.database_path = database_path
        self.pnuids = pnuids
        self.thresholds = thresholds

    def process_json_files(self):
        for json_file in self.json_files:
            json_file_path = os.path.join(self.results_dir, json_file)
            self._process_single_file(json_file_path, json_file)

    def _process_single_file(self, json_file_path, json_file):
        # Load the JSON data from the file
        with open(json_file_path, 'r') as f:
            data = json.load(f)

        # Accessing the dictionary with the data
        camera_data = data[0][f'{self.database_path}/{str(json_file)[:-5]}']
        print(f"Processing {json_file}...")

        # Loop through the keys and process each array
        for key in self.pnuids:
            arr = np.array(camera_data.get(key, []))  # Use .get to avoid KeyError if the key is missing
            self._analyze_array(arr, key)

        print("-" * 50)  # Separator between JSON files

    def _analyze_array(self, arr, key):
        for th in self.thresholds:
            if len(arr) > 0:  # Only process if the array is not empty
                count = np.sum(arr > th)
                length = len(arr)
                percentage = (count / length) * 100 if length > 0 else 0

                # Print the results for each key and threshold
                name = key.split("/")[-2]
                print(f"{name} : {count} elements > {th} out of {length} ({percentage:.3f}%)")
        print()

# Example usage
if __name__ == "__main__":

    THRESHOLDS = [0.0019, 0.002, 0.00245, 0.003]  # Thresholds for analysis

    processor = JSONDataProcessor(JSON_FILES, ALL_RESULTS_DIR, DATABASE_PATH, PNUIDS, THRESHOLDS)
    processor.process_json_files()
