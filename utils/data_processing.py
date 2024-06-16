import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split


def load_images_from_folder(folder):
    """
    Load images and their corresponding labels from a folder structure where each subfolder represents a class.

    Args:
        folder (str): Path to the root folder containing subfolders of class images.

    Returns:
        tuple: A tuple containing:
            - images (list): List of loaded images.
            - labels (list): List of labels corresponding to each image.
            - class_names (list): List of class names (subfolder names).
    """
    images = []
    labels = []
    class_names = sorted(
        os.listdir(folder)
    )  # Assuming folder names are the class names

    for idx, class_name in enumerate(class_names):
        class_folder = os.path.join(folder, class_name)
        for filename in os.listdir(class_folder):
            img_path = os.path.join(class_folder, filename)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)  # Load as grayscale
            if img is not None:
                images.append(img)
                labels.append(idx)  # Assign label based on class index

    return images, labels, class_names


def preprocess_image(img):
    """
    Preprocess a single image by resizing and normalizing it.

    Args:
        img (PIL.Image): Input image.

    Returns:
        np.ndarray: Preprocessed image as a numpy array.
    """
    # Resize image to model input size (45x45) and normalize
    img_array = np.array(img.resize((45, 45))) / 255.0
    img_input = np.expand_dims(img_array, axis=0)
    return img_input


def preprocess_dataset(dataset_folder, save_path):
    """
    Preprocess a dataset of images, split them into training, development (validation), and test sets,
    and save the processed data.

    Args:
        dataset_folder (str): Path to the folder containing the dataset.
        save_path (str): Path to save the preprocessed data.

    Returns:
        None
    """
    # Load images and labels from dataset folder
    images, labels, class_names = load_images_from_folder(dataset_folder)

    # Convert lists to numpy arrays for easier manipulation
    images = np.array(images)
    labels = np.array(labels)

    print(f"Number of images loaded: {len(images)}")
    print(f"Number of labels loaded: {len(labels)}")
    print(f"Class names: {class_names}")

    # Convert grayscale images to RGB
    images_rgb = np.repeat(images[..., np.newaxis], 3, -1)

    # Normalize images to range [0, 1]
    normalized_images = images_rgb / 255.0

    # Reshape images for model input (if necessary)
    reshaped_images = normalized_images.reshape(-1, images.shape[1], images.shape[2], 3)

    print(f"Shape of reshaped images: {reshaped_images.shape}")

    # Split data into training, development (validation), and test sets
    X_train, X_temp, y_train, y_temp = train_test_split(
        reshaped_images, labels, test_size=0.3, random_state=42
    )
    X_dev, X_test, y_dev, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, random_state=42
    )

    print(f"Shape of X_train: {X_train.shape}, y_train: {y_train.shape}")
    print(f"Shape of X_dev: {X_dev.shape}, y_dev: {y_dev.shape}")
    print(f"Shape of X_test: {X_test.shape}, y_test: {y_test.shape}")

    # Save preprocessed data
    np.savez_compressed(
        save_path,
        X_train=X_train,
        y_train=y_train,
        X_dev=X_dev,
        y_dev=y_dev,
        X_test=X_test,
        y_test=y_test,
        class_names=class_names,
    )

    print(f"Preprocessed data saved to {save_path}")


# Example usage
if __name__ == "__main__":
    dataset_folder = "data/dataset"
    save_path = "data/processed_data/math_notation_dataset.npz"
    preprocess_dataset(dataset_folder, save_path)
