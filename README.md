# Project Overview

This repository contains a collection of Python scripts designed for image processing, signal transformation, and data analysis, with a specific focus on wavelet transforms and PNU identification (PNU ID) mapping.

## How to Use
1. **Clone the repository**:
  ```bash
  git clone https://github.com/AmirAmmar123/img-camera-matching.git
  ```
2. **Ensure you have Python 3.9 installed**:
  ```bash
  python3.9 --version
  ```
3. **Create a Python virtual environment**:
  ```bash
  cd img-camera-matching
  python3.9 -m venv myenv
  source myenv/bin/activate
  ```
4. **Install the required packages**:
  ```bash
  pip install -r requirements.txt
  ```
5. **Run the initialization script**:
  ```bash
  ./init.sh
  ```
6. **Ensure the dataset is prepared**:
  - Make sure there are approximately 300 images for training and 100 images for testing in the `training` and `testing` directories, respectively.




## Arguments for `main.py`

The `main.py` script accepts the following arguments:

| Argument                   | Type   | Default Value                                              | Description                                                                 |
|----------------------------|--------|------------------------------------------------------------|-----------------------------------------------------------------------------|
| `--db_path`                | `str`  | `'data-base'`                                              | Path to the database.                                                       |
| `--data_dump`              | `str`  | `'/data-base/results/'`                                     | Path to dump the output results.                                            |
| `--home_directory_path`    | `str`  | `'/<HomeDir>/img-camera-matching/'`                         | Path to the home directory.                                                 |
| `--base_directory`         | `str`  | `'img-camera-matching/Data-Base'`                           | Base directory from the project directory to the data-base directory.       |
| `--read_correlation_result`| `str`  | `'data-base/results/data.json'`                             | Path to save the correlation results between the data-base and PNU ID.      |
| `--save_to_gaussian_stage` | `str`  | `'data-base/results/prep_to_threshold.json'`                | Path to save the closest points between the data-base and PNU ID.           |
| `--save_to_gaussian`       | `str`  | `'/<HomeDir>/img-camera-matching/data-base/results/gaussian.json'` | Path to save the Gaussian results.                                          |
| `--load_gaussian`          | `str`  | `'/<HomeDir>/img-camera-matching/data-base/results/gaussian.json'` | Path to load the pairs of Gaussian that have been created.                  |
| `--create_x_pnu_id`        | `int`  | `0`                                                        | Number of PNU IDs to create.                                                |
| `--activate_creation`      | `bool` | `False`                                                    | Activate the generation of PNU ID for each image dataset.                   |
| `--activate_matcher`       | `bool` | `False`                                                    | Activate the correlation generation between image-set and PNU ID.           |
