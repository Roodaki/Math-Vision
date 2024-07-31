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
)
from PyQt5.QtCore import QFile
from ui.canvas_widget import CanvasWidget
from ui.prediction_result_widget import PredictionResultWidget
from utils.data_processing import preprocess_single_image
from utils.bounding_box import crop_bounding_box_from_image


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
        self.button_layout = QHBoxLayout()
        self.addButtonToLayout("Clear", self.canvas.clearCanvas, self.button_layout)
        self.addButtonToLayout(
            "Brush Size", self.showBrushSizeDialog, self.button_layout
        )
        self.addButtonToLayout("Undo", self.canvas.undoDrawing, self.button_layout)
        self.addButtonToLayout("Redo", self.canvas.redoDrawing, self.button_layout)
        self.addButtonToLayout(
            "Predict", self.predictDrawingFromCanvas, self.button_layout
        )
        self.layout.addLayout(self.button_layout)

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
            bounding_boxes = self.canvas.bounding_boxes
            if bounding_boxes:
                self.canvas.hide()  # Hide the canvas
                self.button_layout.setParent(None)  # Remove the button layout

                self.prediction_widget = PredictionResultWidget()
                self.prediction_widget.backClicked.connect(
                    self.showCanvasWidget
                )  # Connect the back button signal
                self.layout.addWidget(self.prediction_widget)

                for box in bounding_boxes:
                    cropped_image = crop_bounding_box_from_image(drawing_image, box)
                    resized_image = cropped_image.resize((45, 45))
                    preprocessed_image = preprocess_single_image(resized_image)

                    trained_model_path = "models/saved_models/trained_model.h5"
                    model = load_model(trained_model_path)
                    prediction = model.predict(preprocessed_image)
                    predicted_class_index = np.argmax(prediction)

                    if predicted_class_index < len(self.class_names):
                        predicted_class_name = self.class_names[predicted_class_index]
                        prediction_confidence = (
                            prediction[0, predicted_class_index] * 100
                        )
                        self.prediction_widget.addPrediction(
                            predicted_class_name, prediction_confidence, cropped_image
                        )
                    else:
                        QMessageBox.warning(self, "Prediction", "Invalid class index")
            else:
                QMessageBox.warning(self, "Prediction", "No bounding box found")

    def showCanvasWidget(self):
        """Show the canvas widget and hide the prediction widget."""
        self.prediction_widget.setParent(None)  # Remove prediction widget
        self.layout.addWidget(self.canvas)  # Re-add canvas widget
        self.layout.addLayout(self.button_layout)  # Re-add button layout
        self.canvas.show()  # Show the canvas
