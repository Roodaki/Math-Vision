from PyQt5.QtGui import QImage
import numpy as np


def convert_qimage_to_numpy(qimage):
    qimage = qimage.convertToFormat(QImage.Format_RGB32)
    width = qimage.width()
    height = qimage.height()
    ptr = qimage.bits()
    ptr.setsize(qimage.byteCount())
    arr = np.array(ptr).reshape(height, width, 4)
    return arr[:, :, :3]  # Remove alpha channel
