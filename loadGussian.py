import json
import matplotlib.pyplot as plt 
import numpy as np 
import logging 
logging.basicConfig(level=logging.INFO,  # Set level to INFO to capture all INFO messages
                    format='%(asctime)s - %(levelname)s - %(message)s')

class LoadAllPairsOfGaussian:
    
    def __init__(self, path_to_file: str = "./data-base/results/gaussian.json") -> None:
        self.path = path_to_file    
        with open(path_to_file, 'r') as f:
            self.gaussian_array = json.load(f)
        
    def get_gaussian(self, x):
        return self.gaussian_array[x]
        
class LoadGaussianPair:
    TITLE = 'pnu_id_path'
    AXIS_X_1 = 'basePathHighest'
    AXIS_X_2 = 'basePathsecondHighest'
    RESULT1_KEY = 'highest_correlation_results'
    RESULT2_KEY = 'second_highest_correlation_results'
    
    def __init__(self, **kwargs) -> None:
        self.title = kwargs.get(self.TITLE, 'Default Title')
        self.axis_1 = kwargs.get(self.AXIS_X_1, 'Axis X1')
        self.axis_2 = kwargs.get(self.AXIS_X_2, 'Axis X2')
        self.results1 = kwargs.get(self.RESULT1_KEY, [])
        self.results2 = kwargs.get(self.RESULT2_KEY, [])
        
        self.mean1, self.mean2 = self.calculate_mean()
        self.var1, self.var2 = self.calculate_variance()

    def calculate_mean(self):
        return np.mean(self.results1), np.mean(self.results2)

    def calculate_variance(self):
        return np.var(self.results1), np.var(self.results2)

    def save_plot(self, save_path: str):
        plt.savefig(save_path)
        logging.info(f'Plot saved to {save_path}')
        
    def display_statistics(self):
        print(f'Mean of results1: {self.mean1:.7f}, Variance of results1: {self.var1:.7f}')
        print(f'Mean of results2: {self.mean2:.7f}, Variance of results2: {self.var2:.7f}')

    def gaussian_pdf(self, x, mean, variance):
        sigma = np.sqrt(variance)
        return (1 / (np.sqrt(2 * np.pi * sigma**2))) * np.exp(-((x - mean) ** 2) / (2 * sigma ** 2))
    
    def plot_gaussian(self, mean, variance, label):
        x_values = np.linspace(mean - 3 * np.sqrt(variance), mean + 3 * np.sqrt(variance), 1000)
        y_values = self.gaussian_pdf(x_values, mean, variance)
        plt.plot(x_values, y_values, label=f'Gaussian: {"/".join(label.split("/")[-1:])}, μ={mean:.7f}, σ²={variance:.7f}')
        
    
    def visualize(self, save_path: str = None):
        logging.info("Visualizing the two Gaussian distributions")
        plt.figure(figsize=(10, 6))

        # Use science-friendly colors
        color_1 = plt.cm.viridis(0.6)  # Viridis color for the first Gaussian
        color_2 = plt.cm.plasma(0.4)   # Plasma color for the second Gaussian

        self.plot_gaussian(self.mean1, self.var1, self.axis_1, color=color_1)
        self.plot_gaussian(self.mean2, self.var2, self.axis_2, color=color_2)

        # Find intersections and plot the one with the highest y-value
        intersections = self.find_gaussian_intersections()
        if intersections is not None:
            highest_y_value = -np.inf
            highest_point = None

            for root in intersections:
                y_value = self.gaussian_pdf(root, self.mean1, self.var1)
                if y_value > highest_y_value:
                    highest_y_value = y_value
                    highest_point = (root, y_value)

            if highest_point:
                plt.plot(highest_point[0], highest_point[1], 'ro')  # Plot highest intersection point
                plt.annotate(f'Intersection Point\n({highest_point[0]:.5f}, {highest_point[1]:.5f})', 
                            (highest_point[0], highest_point[1]), 
                            textcoords="offset points", 
                            xytext=(0,10), 
                            ha='center', 
                            color='red',   # Red text color
                            fontsize=12,   # Larger font size
                            bbox=dict(facecolor='white', alpha=0.3))  # Transparent yellow background

        plt.title(f'Gaussian Distributions for {self.title} with Intersection Point Highlighted')
        
        if save_path:
            self.save_plot(save_path)
        else:
            logging.info("Plotting the two Gaussian distributions")
            plt.show()

    def plot_gaussian(self, mean, variance, label, color):
        x_values = np.linspace(mean - 3 * np.sqrt(variance), mean + 3 * np.sqrt(variance), 1000)
        y_values = self.gaussian_pdf(x_values, mean, variance)
        plt.plot(x_values, y_values, label=f'Gaussian: {"/".join(label.split("/")[-1:])}, μ={mean:.7f}, σ²={variance:.7f}', color=color)

    def find_gaussian_intersections(self):
        a = 1/(2*self.var1) - 1/(2*self.var2)
        b = self.mean2/self.var2 - self.mean1/self.var1
        c = self.mean1**2 /(2*self.var1) - self.mean2**2 / (2*self.var2) - np.log(np.sqrt(self.var2)/np.sqrt(self.var1))
        roots = np.roots([a, b, c])
        return roots[np.isreal(roots)].real if np.isreal(roots).any() else None

# Example usage remains the same
