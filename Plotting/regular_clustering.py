import json
import numpy as np
import matplotlib.pyplot as plt

# Load JSON data
json_file = 'Data-Base/results/data.json'  # Path to your JSON file
with open(json_file, 'r') as file:
    data = json.load(file)

# Prepare data for plotting
cluster_data = {}
for test_path, pnu_data in data.items():
    test_name = test_path.split('/')[-2]  # Extract the test name for labeling
    pnu_ids = list(pnu_data.keys())
    correlation_values = list(pnu_data.values())
    # Shorten the PNU IDs by taking only the last part of the path
    shortened_pnu_ids = [pnu_id.split('/')[-1] for pnu_id in pnu_ids]
    cluster_data[test_name] = (shortened_pnu_ids, correlation_values)

# Plotting the clusters
plt.figure(figsize=(14, 8))  # Make the plot wider

colors = plt.cm.get_cmap('tab10', len(cluster_data))  # Generate enough colors

for i, (test_name, (pnu_ids, correlation_values)) in enumerate(cluster_data.items()):
    # Scatter plot for each cluster
    plt.scatter(pnu_ids, correlation_values, label=f'Cluster: {test_name}', color=colors(i))

# Labeling the plot
plt.title('PNU Correlation Clustering by Testing Sets')
plt.xlabel('PNU ID')
plt.ylabel('Correlation')
plt.xticks(rotation=45, ha='right', fontsize=10)  # Rotate and align x-axis labels for better readability
plt.legend(loc='upper right', bbox_to_anchor=(1.25, 1))  # Place legend outside the plot
plt.tight_layout()
plt.show()
