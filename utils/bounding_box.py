import numpy as np
from PyQt5.QtGui import QImage


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


def convert_qimage_to_numpy_array(input_qimage: QImage) -> np.ndarray:
    """
    Convert a QImage to a numpy array.

    Args:
        input_qimage (QImage): Input QImage to convert.

    Returns:
        np.ndarray: Converted numpy array representing the QImage.
    """
    # Convert the QImage to RGB32 format for consistency
    rgb32_qimage = input_qimage.convertToFormat(QImage.Format_RGB32)

    # Extract width, height, and byte array from the QImage
    image_width = rgb32_qimage.width()
    image_height = rgb32_qimage.height()
    byte_array = rgb32_qimage.bits()
    byte_array.setsize(rgb32_qimage.byteCount())

    # Convert byte array to a numpy array and reshape it to (height, width, 4)
    numpy_array = np.array(byte_array).reshape(image_height, image_width, 4)

    # Return the numpy array without the alpha channel (last channel)
    return numpy_array[:, :, :3]
