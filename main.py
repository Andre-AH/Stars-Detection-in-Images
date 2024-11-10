import cv2
import os
import matplotlib.pyplot as plt
from skimage.feature import blob_log

# Parameters
image_path = 'original.jpg'       # Fixed path to the input image
threshold_value = 50          # Binary threshold value
blur_kernel_size = 1           # Gaussian blur kernel size
max_sigma = 30                 # Max sigma for blob detection
num_sigma = 10                 # Number of sigma levels for blob detection


def load_image(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"The file '{path}' does not exist.")
    image = cv2.imread(path)
    if image is None:
        raise ValueError(f"Failed to load the image. Check if the file '{path}' is a valid image.")
    return image

# Function to preprocess the image (convert to grayscale, blur, and threshold)
def preprocess_image(image, blur_kernel, threshold):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (blur_kernel, blur_kernel), 0)
    _, thresh = cv2.threshold(blurred, threshold, 255, cv2.THRESH_BINARY)
    return thresh

# Function to detect blobs using Laplacian of Gaussian
def detect_blobs(image, max_sigma, num_sigma, threshold):
    return blob_log(image, max_sigma=max_sigma, num_sigma=num_sigma, threshold=threshold)


def plot_side_by_side(original_image, blobs):
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    axes[0].imshow(original_image, cmap="gray")
    axes[0].set_title("Thresholded Image")
    axes[0].axis("off")

    axes[1].imshow(original_image, cmap="gray")
    for blob in blobs:
        y, x, r = blob
        axes[1].add_patch(plt.Circle((x, y), r, color='red', linewidth=1, fill=False))
    axes[1].set_title(f"Detected Blobs (Count: {len(blobs)})")
    axes[1].axis("off")

    plt.tight_layout()
    plt.show()


image = load_image(image_path)
thresh_image = preprocess_image(image, blur_kernel_size, threshold_value)


blobs_log = detect_blobs(thresh_image, max_sigma, num_sigma, threshold=0.1)
print(f"Number of blobs (stars) detected: {len(blobs_log)}")

plot_side_by_side(image, blobs_log)
