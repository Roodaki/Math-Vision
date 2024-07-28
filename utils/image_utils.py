from PyQt5.QtGui import QImage, qRgb
import numpy as np
from PIL import Image


def crop_bounding_box(image, bounding_box):
    """
    Crop the bounding box from the image.

    Args:
    - image (QImage): Input QImage.
    - bounding_box (tuple): Bounding box coordinates (x_min, y_min, x_max, y_max).

    Returns:
    - PIL.Image: Cropped PIL Image of the bounding box.
    """
    x_min, y_min, x_max, y_max = bounding_box
    image_pil = qimage_to_pil(image)
    cropped_image = image_pil.crop((x_min, y_min, x_max, y_max))
    return cropped_image


def qimage_to_pil(qimage):
    """
    Convert a QImage to a PIL Image.

    Args:
    - qimage (QImage): Input QImage.

    Returns:
    - PIL.Image: Converted PIL Image.
    """
    width, height = qimage.width(), qimage.height()
    image_data = qimage.bits().asstring(width * height * 4)
    image = np.frombuffer(image_data, dtype=np.uint8).reshape((height, width, 4))
    image_pil = Image.fromarray(image)
    return image_pil


def convert_qimage_to_numpy(qimage):
    """
    Convert a QImage to a numpy array.

    Args:
        qimage (QImage): Input QImage to convert.

    Returns:
        np.ndarray: Converted numpy array representing the QImage.
    """
    # Convert the QImage to a format compatible with numpy
    qimage = qimage.convertToFormat(QImage.Format_RGB32)

    # Get the dimensions of the QImage
    width = qimage.width()
    height = qimage.height()

    # Get the byte array of the QImage and reshape it to a 3-channel numpy array
    ptr = qimage.bits()
    ptr.setsize(qimage.byteCount())
    arr = np.array(ptr).reshape(height, width, 4)

    # Return the numpy array, removing the alpha channel
    return arr[:, :, :3]
