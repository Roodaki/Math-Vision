from PyQt5.QtGui import QImage
import numpy as np
from PIL import Image


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


def convert_qimage_to_pil(qimage: QImage) -> Image:
    """
    Convert a QImage to a PIL Image.

    Args:
        qimage (QImage): The QImage to convert.

    Returns:
        Image: Converted PIL Image.
    """
    width, height = qimage.width(), qimage.height()
    image_data = qimage.bits().asstring(width * height * 4)
    numpy_array = np.frombuffer(image_data, dtype=np.uint8).reshape((height, width, 4))
    return Image.fromarray(numpy_array)


def convert_qimage_to_numpy_array(qimage: QImage) -> np.ndarray:
    """
    Convert a QImage to a numpy array, excluding the alpha channel.

    Args:
        qimage (QImage): The QImage to convert.

    Returns:
        np.ndarray: Numpy array representation of the QImage, without the alpha channel.
    """
    qimage_rgb = qimage.convertToFormat(QImage.Format_RGB32)
    width, height = qimage_rgb.width(), qimage_rgb.height()
    image_ptr = qimage_rgb.bits()
    image_ptr.setsize(qimage_rgb.byteCount())
    numpy_array = np.array(image_ptr).reshape(height, width, 4)
    return numpy_array[:, :, :3]
