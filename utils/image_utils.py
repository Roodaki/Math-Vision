from PyQt5.QtGui import QImage, qRgb
import numpy as np


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


# Example usage
if __name__ == "__main__":
    # Example of converting a QImage to a numpy array
    qimage = QImage("example.png")
    numpy_array = convert_qimage_to_numpy(qimage)
    print(f"Converted QImage to numpy array with shape: {numpy_array.shape}")
