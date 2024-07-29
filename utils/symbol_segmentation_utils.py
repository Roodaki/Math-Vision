import cv2
import numpy as np
from PyQt5.QtGui import QImage
from utils.image_processing_utils import convert_qimage_to_numpy_array


def find_all_symbols_bounding_boxes(
    input_image: QImage, symbol_rgb_color: tuple, padding_pixels: int = 10
) -> list:
    """
    Find all bounding boxes for symbols of a given color in the QImage with specified padding.

    Args:
        input_image (QImage): Input QImage to calculate the bounding boxes for.
        symbol_rgb_color (tuple): RGB color of the symbols as a tuple (R, G, B).
        padding_pixels (int): Padding in pixels to add around each bounding box.

    Returns:
        list: List of bounding box coordinates as (x_min, y_min, x_max, y_max).
    """
    numpy_image = convert_qimage_to_numpy_array(input_image)
    symbol_color_array = np.array(symbol_rgb_color, dtype=np.uint8)

    # Create a binary mask for the symbol color
    binary_mask = np.all(numpy_image == symbol_color_array, axis=-1)

    # Label connected components in the binary mask
    num_labels, labels_im = cv2.connectedComponents(binary_mask.astype(np.uint8))

    bounding_boxes = []
    for label in range(1, num_labels):  # Skip the background label (0)
        coords = np.column_stack(np.where(labels_im == label))
        if coords.size > 0:
            y_min, x_min = coords.min(axis=0)
            y_max, x_max = coords.max(axis=0)

            # Add padding to the bounding box coordinates
            y_min = max(y_min - padding_pixels, 0)
            x_min = max(x_min - padding_pixels, 0)
            y_max = min(y_max + padding_pixels, numpy_image.shape[0] - 1)
            x_max = min(x_max + padding_pixels, numpy_image.shape[1] - 1)

            bounding_boxes.append((x_min, y_min, x_max, y_max))

    return bounding_boxes
