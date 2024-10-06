import json
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np
import tifffile as tiff
from skimage import exposure
import os

class DeviceClusterAnalysis2D:
    def __init__(self, json_file_path: str, n_clusters: int = 6):
        """
        Initialize the DeviceClusterAnalysis object.
        
        :param json_file_path: Path to the JSON file containing data.
        :param n_clusters: Number of clusters for KMeans.
        """
        self.json_file_path = json_file_path
        self.n_clusters = n_clusters
        self.df = None
        self.scaled_df = None
        self.reduced_data = None
        self.clusters = None
        
        # Automatically load and process data upon initialization
        self.load_json_data()
        self.normalize_data()
        self.reduce_dimensions()
        self.perform_clustering()

    def load_json_data(self):
        """
        Load JSON data from the file and parse it into a DataFrame.
        """
        with open(self.json_file_path) as f:
            data = json.load(f)
        self.df = self.parse_data(data)
        
    def parse_data(self, data):
        """
        Parse JSON data into a Pandas DataFrame.
        
        :param data: JSON data loaded from the file.
        :return: A Pandas DataFrame where rows represent "testing" devices and columns represent "pnu_id" comparisons.
        """
        parsed_data = {
            test_device: dict(comparisons.items())
            for test_device, comparisons in data.items()
        }
        return pd.DataFrame(parsed_data).T  # Transpose to make "testing" devices rows
    
    def normalize_data(self):
        """
        Normalize the DataFrame using StandardScaler.
        """
        scaler = StandardScaler()
        self.scaled_df = scaler.fit_transform(self.df)

    def reduce_dimensions(self, n_components=2):
        """
        Perform PCA to reduce dimensions for visualization.
        
        :param n_components: Number of dimensions to reduce the data to (default is 2 for 2D visualization).
        """
        pca = PCA(n_components=n_components)
        self.reduced_data = pca.fit_transform(self.scaled_df)

    def perform_clustering(self):
        """
        Perform KMeans clustering on the reduced data.
        """
        kmeans = KMeans(n_clusters=self.n_clusters)
        self.clusters = kmeans.fit_predict(self.reduced_data)

    def plot_clusters(self, save_path: str = None):
        """
        Plot the clusters and annotate points with device names.
        
        :param save_path: If provided, the plot will be saved to this path instead of being displayed.
        """
        plt.figure(figsize=(10, 6))
        plt.scatter(self.reduced_data[:, 0], self.reduced_data[:, 1], c=self.clusters, cmap='viridis', s=100)
        plt.title('Cluster Plot of Test Devices based on pnu_id Comparisons')
        plt.xlabel('PCA Component 1')
        plt.ylabel('PCA Component 2')

        # Annotate points with device names
        for i, device in enumerate(self.df.index):
            plt.annotate(device.split('/')[-2], (self.reduced_data[i, 0], self.reduced_data[i, 1]), fontsize=9)

        # Save the plot if save_path is provided
        if save_path:
            plt.savefig(save_path)
            print(f"Plot saved to {save_path}")
        else:
            plt.show()


class DeviceClusterAnalysis3D:
    def __init__(self, json_file_path: str, n_clusters: int = 6):
        """
        Initialize the DeviceClusterAnalysis3D object.
        
        :param json_file_path: Path to the JSON file containing data.
        :param n_clusters: Number of clusters for KMeans.
        """
        self.json_file_path = json_file_path
        self.n_clusters = n_clusters
        self.df = None
        self.scaled_df = None
        self.reduced_data_3d = None
        self.clusters = None
        
        # Automatically load and process data upon initialization
        self.load_json_data()
        self.normalize_data()
        self.reduce_dimensions()
        self.perform_clustering()

    def load_json_data(self):
        """
        Load JSON data from the file and parse it into a DataFrame.
        """
        with open(self.json_file_path) as f:
            data = json.load(f)
        self.df = self.parse_data(data)
        
    def parse_data(self, data):
        """
        Parse JSON data into a Pandas DataFrame.
        
        :param data: JSON data loaded from the file.
        :return: A Pandas DataFrame where rows represent "testing" devices and columns represent "pnu_id" comparisons.
        """
        parsed_data = {
            test_device: dict(comparisons.items())
            for test_device, comparisons in data.items()
        }
        return pd.DataFrame(parsed_data).T  # Transpose to make "testing" devices rows
    
    def normalize_data(self):
        """
        Normalize the DataFrame using StandardScaler.
        """
        scaler = StandardScaler()
        self.scaled_df = scaler.fit_transform(self.df)

    def reduce_dimensions(self, n_components=3):
        """
        Perform PCA to reduce dimensions for 3D visualization.
        
        :param n_components: Number of dimensions to reduce the data to (default is 3 for 3D visualization).
        """
        pca = PCA(n_components=n_components)
        self.reduced_data_3d = pca.fit_transform(self.scaled_df)

    def perform_clustering(self):
        """
        Perform KMeans clustering on the reduced 3D data.
        """
        kmeans = KMeans(n_clusters=self.n_clusters)
        self.clusters = kmeans.fit_predict(self.reduced_data_3d)

    def plot_clusters_3d(self, save_path: str = None):
        """
        Plot the clusters in 3D and annotate points with device names.
        
        :param save_path: If provided, the plot will be saved to this path instead of being displayed.
        """
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')

        sc = ax.scatter(self.reduced_data_3d[:, 0], self.reduced_data_3d[:, 1], self.reduced_data_3d[:, 2], 
                        c=self.clusters, cmap='viridis', s=100)

        ax.set_title('3D Cluster Plot of Test Devices based on pnu_id Comparisons')
        ax.set_xlabel('PCA Component 1')
        ax.set_ylabel('PCA Component 2')
        ax.set_zlabel('PCA Component 3')

        # Annotate points with device names
        for i, device in enumerate(self.df.index):
            ax.text(self.reduced_data_3d[i, 0], self.reduced_data_3d[i, 1], self.reduced_data_3d[i, 2], 
                    device.split('/')[-2], fontsize=9)

        # Save the plot if save_path is provided
        if save_path:
            plt.savefig(save_path)
            print(f"3D Plot saved to {save_path}")
        else:
            plt.show()



class ImagePNUIDHistogram:
    def __init__(self, image_path: str, save_dir: str = None):
        """
        Initializes the ImagePNUIDHistogram class with an image path and an optional save directory.
        
        Args:
        image_path (str): Path to the image file.
        save_dir (str): Directory where the histogram and image will be saved. Default is None.
        """
        self.image_path = image_path
        self.save_dir = save_dir
        self.image = self._load_image()
    
    def _load_image(self) -> np.array:
        """
        Loads the image from the specified path.
        
        Returns:
        np.array: Loaded image.
        """
        return tiff.imread(self.image_path)
    
    def plot_histogram(self, save: bool = False):
        """
        Calculates and plots the histogram of the loaded image using skimage's exposure.histogram.
        Optionally saves the histogram plot.
        """
        # Calculate the histogram
        histogram, bins = exposure.histogram(self.image)
        
        # Plot the histogram
        plt.figure()
        plt.title(f'PNU id Histogram for {self.image_path}')
        plt.xlabel("Bins")
        plt.ylabel("# of Pixels")
        plt.bar(bins, histogram, width=1)
        plt.xlim([-5, 5])  # Adjusted to match the range of grayscale values
        
        if save and self.save_dir:
            res = ''.join(self.image_path.split('/')[2:-2])
            histogram_path = os.path.join(self.save_dir, f'{res}_histogram.png')
            plt.savefig(histogram_path)
            print(f'Histogram saved as {histogram_path}')
        else:
            plt.show()
    
    def show_image(self, save: bool = False):
        """
        Displays the loaded image. Optionally saves the image.
        """
        plt.figure()
        plt.title("Image")
        plt.imshow(self.image, cmap='gray')
        plt.axis('off')  # Hide axes
        
        if save and self.save_dir:
            res = ''.join(self.image_path.split('/')[2:-2])
            image_path = os.path.join(self.save_dir, os.path.join(self.save_dir, f'{res}_histogram.png'))
            plt.savefig(image_path, bbox_inches='tight', pad_inches=0)
            print(f'Image saved as {image_path}')
        else:
            plt.show()


if __name__ == '__main__':
    # # Example usage:
    # # Create an instance of the class and plot the clusters
    # device_cluster = DeviceClusterAnalysis2D(json_file_path='data-base/results/data.json', n_clusters=6)
    # # To display the plot
    # device_cluster.plot_clusters()
    # # To save the plot to a file (e.g., 'cluster_plot.png')
    # device_cluster.plot_clusters(save_path='cluster_plot.png')
    i = ImagePNUIDHistogram('/home/ameer/img-camera-matching/data-base/iphone-14-plus-abeer/pnu_id/pnu_id.tiff')
    i._load_image()
    i.show_image()