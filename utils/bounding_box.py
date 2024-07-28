import numpy as np
from PyQt5.QtGui import QImage


def calculate_bounding_box(
    image: QImage, symbol_color: tuple, padding: int = 10
) -> tuple:
    """
    Calculate the bounding box of the given symbol color in the QImage.

    Args:
    - image (QImage): Input QImage to calculate the bounding box for.
    - symbol_color (tuple): RGB color of the symbol.
    - padding (int): Padding around the bounding box.

    Returns:
    - tuple: Bounding box coordinates as (x_min, y_min, x_max, y_max).
    """
    numpy_image = convert_qimage_to_numpy(image)
    symbol_color_np = np.array(symbol_color, dtype=np.uint8)

    # Create a binary mask for the symbol color
    mask = np.all(numpy_image == symbol_color_np, axis=-1)

    coords = np.column_stack(np.where(mask))
    if coords.size == 0:
        return None  # No drawing found

    y_min, x_min = coords.min(axis=0)
    y_max, x_max = coords.max(axis=0)

    # Add padding to the bounding box
    y_min = max(y_min - padding, 0)
    x_min = max(x_min - padding, 0)
    y_max = min(y_max + padding, numpy_image.shape[0] - 1)
    x_max = min(x_max + padding, numpy_image.shape[1] - 1)

    return x_min, y_min, x_max, y_max


def convert_qimage_to_numpy(qimage):
    """
    Convert a QImage to a numpy array.

    Args:
    - qimage (QImage): Input QImage to convert.

    Returns:
    - np.ndarray: Converted numpy array representing the QImage.
    """
    qimage = qimage.convertToFormat(QImage.Format_RGB32)
    width = qimage.width()
    height = qimage.height()
    ptr = qimage.bits()
    ptr.setsize(qimage.byteCount())
    arr = np.array(ptr).reshape(height, width, 4)
    return arr[:, :, :3]
