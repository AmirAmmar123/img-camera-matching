import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Load JSON data
json_file = 'Data-Base/results/data.json'  # Path to your JSON file
with open(json_file, 'r') as file:
    data = json.load(file)

# Flattening the data into a list of (testing, pnu_id, correlation) tuples
flattened_data = []
for test_path, pnu_data in data.items():
    for pnu_path, correlation_value in pnu_data.items():
        flattened_data.append((test_path, pnu_path, correlation_value))

# Extracting just the correlation values for clustering
correlation_values = np.array([item[2] for item in flattened_data]).reshape(-1, 1)

# Normalize data
scaler = StandardScaler()
correlation_values_scaled = scaler.fit_transform(correlation_values)

# Perform KMeans clustering
num_clusters = 6  # Setting number of clusters to 6
kmeans = KMeans(n_clusters=num_clusters)
kmeans.fit(correlation_values_scaled)
labels = kmeans.labels_

# Plotting the clusters
plt.figure(figsize=(10, 6))

# Dynamic color map to handle any number of clusters
colors = plt.cm.get_cmap('tab10', num_clusters)

# Plot the clusters
for i in range(num_clusters):
    cluster_points = correlation_values_scaled[labels == i]
    plt.scatter(cluster_points, np.zeros_like(cluster_points), color=colors(i), label=f'Cluster {i+1}')

plt.title('PNU Correlation Clustering')
plt.xlabel('Correlation (Standardized)')
plt.ylabel('Density')
plt.legend()
plt.show()
