# Project Overview

This repository contains a collection of Python scripts designed for image processing, signal transformation, and data analysis, with a specific focus on wavelet transforms and PNU identification (PNU ID) mapping.

## Files and Scripts

1. **avg_training_pny.py**
   - **Description**: This script calculates the average correlation between images in the 'pnu_id' directories and 'testing' directories, and stores the results between each set of images in the testing directory and each PNU ID inside the results directory.

2. **correlation.py**
   - **Description**: Implements a function to calculate the correlation between two arrays: the first being the PNU ID and the second being the wavelet transformation of an image (the HH coefficient).

3. **dataBase.py**
   - **Description**: A utility class to manage and navigate the database of images. It provides functionality to list directories and retrieve paths for further processing.

4. **imgReader.py**
   - **Description**: Provides a class to read images from a directory, offering methods to load, process, and visualize images. It supports various formats including PNG, JPG, HEIC, and TIFF.

5. **plotPnuId.py**
   - **Description**: Loads an image and plots its grayscale histogram. It also allows visualization of the image itself, aiding in the analysis of PNU ID distributions.

6. **pnuidmapper.py**
   - **Description**: Maps pneumonia IDs (PNU IDs) to their corresponding wavelet-transformed images. It calculates key statistics like mean, standard deviation, and saves the transformed images along with the computed data.

7. **waveLetTransform.py**
   - **Description**: Implements the wavelet transform for images, extracting different detail components such as approximation, horizontal detail, vertical detail, and diagonal detail. These components are used in the analysis of image data.

8. **main.py**
   - **Description**: The main script to run the processing pipeline. It performs the following tasks:
     1. **PNU ID Processing**: Creates a `Mapper` instance, processes images, and saves the PNU ID.
     2. **Correlation Calculation**: Creates a `PNUMatcher` instance, calculates correlations, and saves the results.
     3. **(Optional) Histogram Plotting**: Includes example code for using `ImagePNUIDHistogram` to plot and display histograms for PNU ID images. This section is commented out but can be used if needed.

## How to Use

1. **Setting up the Environment**:
   - Ensure that your Python environment is properly set up with all necessary dependencies. You can install the required packages using:
     ```bash
     pip install -r requirements.txt
     ```

2. **Running the Scripts**:
   - **avg_training_pny.py**: Calculates and saves the correlation results between training and test images.
     ```bash
     python avg_training_pny.py
     ```
   - **plotPnuId.py**: Loads an pnu id  image and plots its histogram.
     ```bash
     python plotPnuId.py
     ```
   - **pnuidmapper.py**: Transforms images to generate PNU IDs and calculates related statistics.
     ```bash
     python pnuidmapper.py
     ```
   - **main.py**: Runs the complete pipeline to process PNU IDs, calculate correlations, and optionally plot histograms.
     ```bash
     python main.py
     ```

3. **Testing and Visualization**:
   - **imgReader.py** provides functions for reading and visualizing images. You can integrate it with other scripts to test image processing.
   - **waveLetTransform.py** can be used to visualize the different components of the wavelet-transformed images.

## Project Structure

- **Data-Base/**: Contains directories of images, organized for training and testing purposes.
- **results/**: Stores the output results, including JSON files with correlation data and PNU ID images.

## License

This project is licensed under the MIT License.
