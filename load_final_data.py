import pandas as pd
import numpy as np
import os
import json
from const import *
class JSONDataProcessor:
    def __init__(self, json_files, results_dir, database_path, pnuids, thresholds):
        self.json_files = json_files
        self.results_dir = results_dir
        self.database_path = database_path
        self.pnuids = pnuids
        self.thresholds = thresholds

    def process_json_files(self):
        # Create a dictionary to hold results for each pnu_id
        results = {pnu_id: {} for pnu_id in self.pnuids}

        # Process each JSON file
        for json_file in self.json_files:
            json_file_path = os.path.join(self.results_dir, json_file)
            self._process_single_file(json_file_path, json_file, results)

        # After processing, save the results to an Excel file
        self._save_results_to_excel(results)

    def _process_single_file(self, json_file_path, json_file, results):
        # Load the JSON data from the file
        with open(json_file_path, 'r') as f:
            data = json.load(f)

        # Accessing the dictionary with the data
        camera_data = data[0][f'{self.database_path}/{str(json_file)[:-5]}']
        print(f"Processing {json_file}...")

        # Loop through the pnuids and analyze each array
        for key in self.pnuids:
            arr = np.array(camera_data.get(key, []))  # Use .get to avoid KeyError if the key is missing
            self._analyze_array(arr, key, json_file, results)

    def _analyze_array(self, arr, key, json_file, results):
        if len(arr) > 0:  # Only process if the array is not empty
            row_data = {}
            for th in self.thresholds:
                count = np.sum(arr > th)
                length = len(arr)
                percentage = (count / length) * 100 if length > 0 else 0

                row_data[th] = f"{percentage:.3f}%"

            # Store the result for this json_file in the pnu_id results
            results[key][json_file] = row_data

    def _save_results_to_excel(self, results):
        # Create a Pandas Excel writer object
        with pd.ExcelWriter('pnuid_results.xlsx', engine='xlsxwriter') as writer:
            # Loop through each pnu_id and write the results to a separate sheet
            for pnu_id, json_results in results.items():
                # Convert json_results into a DataFrame
                df = pd.DataFrame.from_dict(json_results, orient='index')
                # Write the DataFrame to a sheet named after the pnu_id
                df.to_excel(writer, sheet_name=pnu_id.split('/')[-2])

# Example usage
if __name__ == "__main__":

    THRESHOLDS = [0.001,0.0019, 0.002, 0.00245, 0.003]  # Thresholds for analysis

    processor = JSONDataProcessor(JSON_FILES, ALL_RESULTS_DIR, DATABASE_PATH, PNUIDS, THRESHOLDS)
    processor.process_json_files()
