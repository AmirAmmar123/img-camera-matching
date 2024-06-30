import cv2
import matplotlib.pyplot as plt

# Correct the file path
file_path = "/home/ameer/img-camera-matching/Data-Base/iphone14-pro/pnu_id/pnu_id.tiff"

# Load the TIFF image using OpenCV
image = cv2.imread(file_path)

# Check if the image was loaded successfully
if image is None:
    raise FileNotFoundError(f"Failed to load image at {file_path}")

# Convert the image from BGR (OpenCV format) to RGB (Matplotlib format)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Plot the image
plt.imshow(image)
plt.axis('off')  # Hide axes
plt.show()