import json
import numpy as np
import os

# Base directory containing the JSON files
json_directory = r"C:\Users\Adi Dvash\Desktop\semester2\פרוייקט\project\img-camera-matching\all_results"

# List of JSON file names
json_files = [
    "iphone14-pro.json",
    "iphone-8-plus-amir.json",
    "iphone-13-pro-amir.json",
    "iphone-14-plus-abeer.json",
    "iphone-areeg.json",
    "iphone-hanaa.json"
]

# List of keys for each array to extract (since the structure inside each JSON file might be the same)
keys = [
    "/home/ameer/img-camera-matching/all_results/iphone-13-pro-amir/pnu_id",
    "/home/ameer/img-camera-matching/all_results/iphone-14-plus-abeer/pnu_id",
    "/home/ameer/img-camera-matching/all_results/iphone-8-plus-amir/pnu_id",
    "/home/ameer/img-camera-matching/all_results/iphone-areeg/pnu_id",
    "/home/ameer/img-camera-matching/all_results/iphone-hanaa/pnu_id",
    "/home/ameer/img-camera-matching/all_results/iphone14-pro/pnu_id"
]

# Loop through each JSON file and process the data
for json_file in json_files:
    json_file_path = os.path.join(json_directory, json_file)

    # Load the JSON data from the file
    with open(json_file_path, 'r') as f:
        data = json.load(f)

    # Accessing the dictionary with the data
    camera_data = data[0]["/home/ameer/img-camera-matching/data-base/"+str(json_file)[:-5]]

    print(f"Processing {json_file}...")

    # Loop through the keys and process each array
    for i, key in enumerate(keys, start=1):
        arr = np.array(camera_data.get(key, []))  # Use .get to avoid KeyError if the key is missing
        if len(arr) > 0:  # Only process if the array is not empty
            count = np.sum(arr > 0.002)
            length = len(arr)
            percentage = (count / length) * 100 if length > 0 else 0

            # Print the results for each file and array
            name = key.split("/")[-2]
            print(f"{name} : {count} elements > 0.002 out of {length} ({percentage:.2f}%)")
    print("-" * 50)  # Separator between JSON files
