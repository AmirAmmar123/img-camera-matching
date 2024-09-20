import json
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from mpl_toolkits.mplot3d import Axes3D  # For 3D plotting

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

# Example usage:
# Create an instance of the class and plot the clusters
device_cluster_3d = DeviceClusterAnalysis3D(json_file_path='data-base/results/data.json', n_clusters=6)
# To display the plot
device_cluster_3d.plot_clusters_3d()
# To save the plot to a file (e.g., '3d_cluster_plot.png')
device_cluster_3d.plot_clusters_3d(save_path='3d_cluster_plot.png')
