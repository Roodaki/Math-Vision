import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Softmax
from PyQt5.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QColorDialog,
    QInputDialog,
    QHBoxLayout,
    QMessageBox,
)
from PyQt5.QtGui import QColor, QImage, QPainter, QPen
from PyQt5.QtCore import Qt, QPoint, QRect, QSize
from ui.canvas_widget import CanvasWidget
from PIL import Image


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Professional Paint App")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # Load preprocessed data and determine input shape and number of classes
        data_path = "data/processed_data/math_notation_dataset.npz"
        data = np.load(data_path, allow_pickle=True)
        self.class_names = data["class_names"]

        self.canvas = CanvasWidget(self)
        self.layout.addWidget(self.canvas)

        button_layout = QHBoxLayout()

        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.canvas.clear_canvas)
        button_layout.addWidget(self.clear_button)

        self.color_button = QPushButton("Select Color")
        self.color_button.clicked.connect(self.show_color_dialog)
        button_layout.addWidget(self.color_button)

        self.brush_size_button = QPushButton("Brush Size")
        self.brush_size_button.clicked.connect(self.show_brush_size_dialog)
        button_layout.addWidget(self.brush_size_button)

        self.undo_button = QPushButton("Undo")
        self.undo_button.clicked.connect(self.canvas.undo)
        button_layout.addWidget(self.undo_button)

        self.redo_button = QPushButton("Redo")
        self.redo_button.clicked.connect(self.canvas.redo)
        button_layout.addWidget(self.redo_button)

        self.predict_button = QPushButton("Predict")
        self.predict_button.clicked.connect(
            self.predict_drawing
        )  # Connect to predict method
        button_layout.addWidget(self.predict_button)  # Add predict button

        self.layout.addLayout(button_layout)

    def show_color_dialog(self):
        color = QColorDialog.getColor(initial=self.canvas.pen_color)
        if color.isValid():
            self.canvas.set_pen_color(color)

    def show_brush_size_dialog(self):
        size, ok = QInputDialog.getInt(
            self, "Select Brush Size", "Size:", self.canvas.pen_width, 1, 50, 1
        )
        if ok:
            self.canvas.set_pen_width(size)

    def predict_drawing(self):
        # Get the drawing from the canvas
        drawing = self.canvas.get_drawing()

        if drawing is not None:
            # Convert QImage to PIL.Image and then to RGB
            img = self.qimage_to_pil(drawing).convert("RGB")

            # Resize image to model input size (45x45) and normalize
            img_resized = img.resize((45, 45))
            img_array = np.array(img_resized) / 255.0

            # Expand dimensions to match the model's expected input shape
            img_input = np.expand_dims(img_array, axis=0)

            # Load the trained model
            model = load_model("models/saved_models/trained_model.h5")

            # Perform prediction
            prediction = model.predict(img_input)

            # Get the predicted class index
            class_index = np.argmax(prediction)

            # Check if the predicted index is valid
            if class_index < len(self.class_names):
                class_name = self.class_names[class_index]
                confidence = prediction[0, class_index]
                QMessageBox.information(
                    self,
                    "Prediction",
                    f"Predicted class: {class_name}\nAccuracy: {confidence:.2%}",
                )
            else:
                QMessageBox.warning(self, "Prediction", "Invalid class index")

    def qimage_to_pil(self, qimage):
        # Convert QImage to numpy array
        width, height = qimage.width(), qimage.height()
        image_data = qimage.bits().asstring(width * height * 4)
        image = np.frombuffer(image_data, dtype=np.uint8).reshape((height, width, 4))

        # Convert RGBA image to PIL Image
        image_pil = Image.fromarray(image)

        return image_pil
