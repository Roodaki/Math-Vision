from PyQt5.QtGui import QImage
import numpy as np
from PIL import Image


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


def convert_pil_to_qimage(pil_image: Image) -> QImage:
    """
    Convert a PIL Image to a QImage.

    Args:
        pil_image (Image): The PIL Image to convert.

    Returns:
        QImage: Converted QImage.
    """
    if pil_image.mode == "RGB":
        pil_image = pil_image.convert("RGBA")

    image_data = pil_image.tobytes("raw", "RGBA")
    qimage = QImage(
        image_data, pil_image.size[0], pil_image.size[1], QImage.Format_RGBA8888
    )
    return qimage


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
