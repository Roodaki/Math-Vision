import numpy as np
from PyQt5.QtGui import QImage
from utils.image_processing_utils import (
    convert_qimage_to_numpy_array,
    convert_qimage_to_pil,
)
from PIL import Image


def calculate_symbol_bounding_box_with_padding(
    input_image: QImage, symbol_rgb_color: tuple, padding_pixels: int = 10
) -> tuple:
    """
    Calculate the bounding box for a symbol of a given color in the QImage with specified padding.

    Args:
        input_image (QImage): Input QImage to calculate the bounding box for.
        symbol_rgb_color (tuple): RGB color of the symbol as a tuple (R, G, B).
        padding_pixels (int): Padding in pixels to add around the bounding box.

    Returns:
        tuple: Bounding box coordinates as (x_min, y_min, x_max, y_max).
               Returns None if no symbol is found.
    """
    numpy_image = convert_qimage_to_numpy_array(input_image)
    symbol_color_array = np.array(symbol_rgb_color, dtype=np.uint8)

    # Create a binary mask for the symbol color
    binary_mask = np.all(numpy_image == symbol_color_array, axis=-1)

    # Get coordinates of all pixels matching the symbol color
    matching_pixel_coords = np.column_stack(np.where(binary_mask))
    if matching_pixel_coords.size == 0:
        return None  # No symbol found

    # Calculate bounding box coordinates
    y_min, x_min = matching_pixel_coords.min(axis=0)
    y_max, x_max = matching_pixel_coords.max(axis=0)

    # Add padding to the bounding box coordinates
    y_min = max(y_min - padding_pixels, 0)
    x_min = max(x_min - padding_pixels, 0)
    y_max = min(y_max + padding_pixels, numpy_image.shape[0] - 1)
    x_max = min(x_max + padding_pixels, numpy_image.shape[1] - 1)

    return x_min, y_min, x_max, y_max


def crop_bounding_box_from_image(image_qt: QImage, bounding_box_coords: tuple) -> Image:
    """
    Crop the specified bounding box from the provided QImage.

    Args:
        image_qt (QImage): The QImage from which to crop.
        bounding_box_coords (tuple): Coordinates of the bounding box (x_min, y_min, x_max, y_max).

    Returns:
        Image: Cropped image as a PIL Image.
    """
    x_min, y_min, x_max, y_max = bounding_box_coords
    pil_image = convert_qimage_to_pil(image_qt)
    cropped_image = pil_image.crop((x_min, y_min, x_max, y_max))
    return cropped_image


def crop_multiple_bounding_boxes_from_image(
    image_qt: QImage, bounding_boxes: list
) -> list:
    """
    Crop multiple bounding boxes from the provided QImage.

    Args:
        image_qt (QImage): The QImage from which to crop.
        bounding_boxes (list): List of bounding box coordinates [(x_min, y_min, x_max, y_max), ...].

    Returns:
        list: List of cropped images as PIL Images.
    """
    pil_image = convert_qimage_to_pil(image_qt)
    cropped_images = [
        pil_image.crop((x_min, y_min, x_max, y_max))
        for (x_min, y_min, x_max, y_max) in bounding_boxes
    ]
    return cropped_images
