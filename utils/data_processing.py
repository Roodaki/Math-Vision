import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from PIL import Image


def load_images_from_class_folders(root_folder_path: str):
    """
    Load images and their corresponding labels from a folder structure where each subfolder represents a class.

    Args:
        root_folder_path (str): Path to the root folder containing subfolders of class images.

    Returns:
        tuple: A tuple containing:
            - images (list): List of loaded images.
            - labels (list): List of labels corresponding to each image.
            - class_names (list): List of class names (subfolder names).
    """
    images = []
    labels = []
    class_names = sorted(
        os.listdir(root_folder_path)
    )  # Assuming folder names are the class names

    for class_index, class_name in enumerate(class_names):
        class_folder_path = os.path.join(root_folder_path, class_name)
        for filename in os.listdir(class_folder_path):
            image_path = os.path.join(class_folder_path, filename)
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Load as grayscale
            if image is not None:
                images.append(image)
                labels.append(class_index)  # Assign label based on class index

    return images, labels, class_names


def preprocess_single_image(image_pil: Image):
    """
    Preprocess a single image by converting to RGB, resizing, and normalizing it.

    Args:
        image_pil (PIL.Image): Input image as a PIL Image.

    Returns:
        np.ndarray: Preprocessed image as a numpy array.
    """
    image_rgb = image_pil.convert("RGB")
    image_resized = image_rgb.resize((45, 45))
    image_normalized = np.array(image_resized) / 255.0
    image_input = np.expand_dims(image_normalized, axis=0)
    return image_input


def preprocess_and_save_dataset(dataset_root_folder: str, save_file_path: str):
    """
    Preprocess a dataset of images, split them into training, development (validation), and test sets,
    and save the processed data.

    Args:
        dataset_root_folder (str): Path to the folder containing the dataset.
        save_file_path (str): Path to save the preprocessed data.

    Returns:
        None
    """
    # Load images and labels from dataset folder
    images, labels, class_names = load_images_from_class_folders(dataset_root_folder)

    # Convert lists to numpy arrays for easier manipulation
    images_array = np.array(images)
    labels_array = np.array(labels)

    print(f"Number of images loaded: {len(images_array)}")
    print(f"Number of labels loaded: {len(labels_array)}")
    print(f"Class names: {class_names}")

    # Convert grayscale images to RGB
    images_rgb = np.repeat(images_array[..., np.newaxis], 3, -1)

    # Normalize images to range [0, 1]
    normalized_images = images_rgb / 255.0

    # Reshape images for model input (if necessary)
    reshaped_images = normalized_images.reshape(
        -1, images_array.shape[1], images_array.shape[2], 3
    )

    print(f"Shape of reshaped images: {reshaped_images.shape}")

    # Split data into training, development (validation), and test sets
    X_train, X_temp, y_train, y_temp = train_test_split(
        reshaped_images, labels_array, test_size=0.3, random_state=42
    )
    X_dev, X_test, y_dev, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, random_state=42
    )

    print(f"Shape of X_train: {X_train.shape}, y_train: {y_train.shape}")
    print(f"Shape of X_dev: {X_dev.shape}, y_dev: {y_dev.shape}")
    print(f"Shape of X_test: {X_test.shape}, y_test: {y_test.shape}")

    # Save preprocessed data
    np.savez_compressed(
        save_file_path,
        X_train=X_train,
        y_train=y_train,
        X_dev=X_dev,
        y_dev=y_dev,
        X_test=X_test,
        y_test=y_test,
        class_names=class_names,
    )

    print(f"Preprocessed data saved to {save_file_path}")


# Example usage
if __name__ == "__main__":
    DATASET_FOLDER = "data/dataset"
    SAVE_FILE_PATH = "data/processed_data/math_notation_dataset.npz"
    preprocess_and_save_dataset(DATASET_FOLDER, SAVE_FILE_PATH)
