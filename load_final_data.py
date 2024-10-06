import pandas as pd
import numpy as np
import os
import json
from const import *
import matplotlib.pyplot as plt 
import random 

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

            # Add the size of the array as the last column
            row_data['Array Size'] = length

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
    
    

class JSONDataPlotter:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.sheets = pd.read_excel(file_path, sheet_name=None)  # Load all sheets into a dictionary
        self.thresholds = None  # To be set for each sheet during processing

    # Function to clean percentage strings and convert to float
    def clean_percentage(self, percentage_str: str):
        return float(percentage_str.strip('%'))

    # Function to plot percentage as a bar chart for each threshold in subplots
    def plot_percentages(self, ax, percentages, threshold, color, sheet_name):
        ax.bar(self.df.iloc[:, 0].str.replace('.json', ''), percentages, color=color, width=0.4)  # Bar chart with file names on the x-axis
        ax.set_title(f"{sheet_name} - {threshold}", fontsize=10)  # Set sheet name and threshold as title
        ax.set_ylabel("Percentage", fontsize=8)
        ax.tick_params(axis='x', rotation=45, labelsize=6)  # Rotate x-tick labels for better readability
        ax.grid(axis='y')  # Grid on the y-axis to show magnitude more clearly

    def process_sheet(self, sheet_name: str, df: pd.DataFrame, row: int):
        self.df = df
        self.thresholds = self.df.columns[1:-1].tolist()  # Get the thresholds from the columns

        # Random color generation for each threshold
        colors = [f'#{random.randint(0, 0xFFFFFF):06x}' for _ in range(len(self.thresholds))]

        # Iterate over each threshold column and plot the data
        for idx, threshold in enumerate(self.thresholds):
            percentages = [self.clean_percentage(val) for val in self.df.iloc[:, idx + 1].values]
            col = idx  # Use the index for the column position
            self.plot_percentages(self.axes[row, col], percentages, threshold, colors[idx], sheet_name)  # Pass sheet name

    def plot_all(self):
        num_sheets = len(self.sheets)

        # Create a 6x6 grid for subplots
        self.fig, self.axes = plt.subplots(6, 6, figsize=(20, 15))  # Create a 6x6 subplot layout
        self.fig.subplots_adjust(hspace=0.4, wspace=0.3)  # Adjust space between subplots

        # Iterate through each sheet in the Excel file
        for row, (sheet_name, df) in enumerate(self.sheets.items()):
            print(f"Processing sheet: {sheet_name}")
            self.process_sheet(sheet_name, df, row)

        plt.tight_layout()  # Adjust layout for better appearance
        plt.show()  # Display all plots

if __name__ == "__main__":

    THRESHOLDS = [0.0009 ,0.001, 0.0019, 0.002, 0.00245, 0.003]  # Thresholds for analysis

    processor = JSONDataProcessor(JSON_FILES, ALL_RESULTS_DIR, DATABASE_PATH, PNUIDS, THRESHOLDS)
    processor.process_json_files()
    JSONDataPlotter('/home/ameer/img-camera-matching/pnuid_results.xlsx').plot_all()