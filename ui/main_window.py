import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from PyQt5.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QInputDialog,
    QHBoxLayout,
    QMessageBox,
    QLabel,
)
from PyQt5.QtCore import Qt, QFile
from PyQt5.QtGui import QPixmap, QImage
from ui.canvas_widget import CanvasWidget
from utils.data_processing import preprocess_single_image
from utils.image_processing_utils import crop_bounding_box_from_image


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        self.initializeUserInterface()

    def initializeUserInterface(self):
        """Initialize the user interface."""
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.setupMainLayout()
        self.loadClassNamesFromDataset()
        self.initializeCanvasWidget()
        self.initializeButtons()
        self.loadStylesheetFromFile()

    def setupMainLayout(self):
        """Setup the main layout for the central widget."""
        self.layout = QVBoxLayout(self.central_widget)

    def loadClassNamesFromDataset(self):
        """Load class names from the preprocessed dataset."""
        dataset_path = "data/processed_data/math_notation_dataset.npz"
        data = np.load(dataset_path, allow_pickle=True)
        self.class_names = data["class_names"]

    def initializeCanvasWidget(self):
        """Initialize the drawing canvas widget."""
        self.canvas = CanvasWidget(self.class_names, self)
        self.layout.addWidget(self.canvas)

    def initializeButtons(self):
        """Initialize the buttons for canvas interaction."""
        button_layout = QHBoxLayout()
        self.addButtonToLayout("Clear", self.canvas.clearCanvas, button_layout)
        self.addButtonToLayout("Brush Size", self.showBrushSizeDialog, button_layout)
        self.addButtonToLayout("Undo", self.canvas.undoDrawing, button_layout)
        self.addButtonToLayout("Redo", self.canvas.redoDrawing, button_layout)
        self.addButtonToLayout("Predict", self.predictDrawingFromCanvas, button_layout)
        self.layout.addLayout(button_layout)

    def addButtonToLayout(self, button_text, on_click_function, layout):
        """Add a button with specified text and click function to the given layout."""
        button = QPushButton(button_text)
        button.clicked.connect(on_click_function)
        layout.addWidget(button)

    def showBrushSizeDialog(self):
        """Show a dialog to set the brush size for the canvas."""
        size, ok = QInputDialog.getInt(
            self, "Select Brush Size", "Size:", self.canvas.pen_width, 1, 50, 1
        )
        if ok:
            self.canvas.setPenWidth(size)

    def loadStylesheetFromFile(self):
        """Load and apply the stylesheet from a file to the main window."""
        stylesheet_path = "ui/resources/styles/stylesheet.qss"
        style_file = QFile(stylesheet_path)
        style_file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = bytes(style_file.readAll()).decode("utf-8")
        self.setStyleSheet(stylesheet)

    def predictDrawingFromCanvas(self):
        """Predict the drawing on the canvas using the trained model."""
        drawing_image = self.canvas.getDrawing()

        if drawing_image is not None:
            bounding_box_coords = self.canvas.bounding_box
            if bounding_box_coords:
                cropped_image = crop_bounding_box_from_image(
                    drawing_image, bounding_box_coords
                )
                resized_image = cropped_image.resize((45, 45))
                preprocessed_image = preprocess_single_image(resized_image)

                trained_model_path = "models/saved_models/trained_model.h5"
                model = load_model(trained_model_path)
                prediction = model.predict(preprocessed_image)
                predicted_class_index = np.argmax(prediction)

                if predicted_class_index < len(self.class_names):
                    predicted_class_name = self.class_names[predicted_class_index]
                    prediction_confidence = prediction[0, predicted_class_index] * 100
                    self.displayPredictionResult(
                        predicted_class_name, prediction_confidence, cropped_image
                    )
                else:
                    QMessageBox.warning(self, "Prediction", "Invalid class index")
            else:
                QMessageBox.warning(self, "Prediction", "No bounding box found")

    def displayPredictionResult(self, class_name, confidence, cropped_image):
        """Display the prediction result in a message box."""
        confidence_color = self.getConfidenceColor(confidence)
        message = f"<p><b>Predicted Class:</b> {class_name}</p>"
        message += f"<p><b>Accuracy:</b> <font color='{confidence_color}'>{confidence:.2f}%</font></p>"

        cropped_image_qt = self.convertPILImageToQImage(cropped_image)
        pixmap = QPixmap.fromImage(cropped_image_qt)
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)

        msg_box = QMessageBox()
        msg_box.setWindowTitle("Prediction")
        msg_box.setTextFormat(Qt.RichText)
        msg_box.setText(message)
        msg_box.layout().addWidget(image_label, 0, 0, Qt.AlignTop | Qt.AlignHCenter)
        msg_box.exec_()

    def getConfidenceColor(self, confidence):
        """Return the color based on confidence level."""
        if confidence >= 90:
            return "green"
        elif confidence >= 80:
            return "yellow"
        elif confidence >= 60:
            return "red"
        else:
            return "gray"

    def convertQImageToPILImage(self, qimage):
        """Convert a QImage to a PIL Image."""
        width, height = qimage.width(), qimage.height()
        image_data = qimage.bits().asstring(width * height * 4)
        image_array = np.frombuffer(image_data, dtype=np.uint8).reshape(
            (height, width, 4)
        )
        pil_image = Image.fromarray(image_array)
        return pil_image

    def convertPILImageToQImage(self, pil_image):
        """Convert a PIL Image to a QImage."""
        if pil_image.mode == "RGB":
            pil_image = pil_image.convert("RGBA")

        image_data = pil_image.tobytes("raw", "RGBA")
        qimage = QImage(
            image_data, pil_image.size[0], pil_image.size[1], QImage.Format_RGBA8888
        )
        return qimage
