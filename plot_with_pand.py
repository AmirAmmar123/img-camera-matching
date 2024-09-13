import json
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Step 1: Load the JSON data from the file
with open('data-base/results/data.json') as f:
    data = json.load(f)

# Step 2: Convert the JSON structure into a Pandas DataFrame
# We will create a DataFrame where rows represent "testing" devices, and columns represent "pnu_id" comparisons

def parse_data(data):
    parsed_data = {}
    for test_device, comparisons in data.items():
        parsed_data[test_device] = {}
        for compare_device, value in comparisons.items():
            parsed_data[test_device][compare_device] = value
    return pd.DataFrame(parsed_data).T  # Transpose to make "testing" devices rows

df = parse_data(data)

# Step 3: Normalize the data (optional but recommended for clustering)
scaler = StandardScaler()
scaled_df = scaler.fit_transform(df)

# Step 4: Dimensionality Reduction using PCA to visualize in 2D
pca = PCA(n_components=2)
reduced_data = pca.fit_transform(scaled_df)

# Step 5: Clustering using K-Means (You can experiment with different clustering algorithms)
kmeans = KMeans(n_clusters=6)  # Choose the number of clusters
clusters = kmeans.fit_predict(reduced_data)

# Step 6: Plotting the clusters
plt.figure(figsize=(10, 6))
plt.scatter(reduced_data[:, 0], reduced_data[:, 1], c=clusters, cmap='viridis', s=100)
plt.title('Cluster Plot of Test Devices based on pnu_id Comparisons')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')

# Annotate points with device names
for i, device in enumerate(df.index):
    plt.annotate(device.split('/')[-2], (reduced_data[i, 0], reduced_data[i, 1]), fontsize=9)

plt.show()