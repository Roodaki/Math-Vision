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
from PyQt5.QtCore import Qt, QFile
from ui.canvas_widget import CanvasWidget
from utils.data_processing import preprocess_image


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        """Initialize the user interface."""
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.setupLayout()
        self.loadClassNames()
        self.setupCanvas()
        self.setupButtons()
        self.loadStylesheet()

    def setupLayout(self):
        """Setup the main layout."""
        self.layout = QVBoxLayout(self.central_widget)

    def loadClassNames(self):
        """Load class names from processed dataset."""
        data = np.load(
            "data/processed_data/math_notation_dataset.npz", allow_pickle=True
        )
        self.class_names = data["class_names"]

    def setupCanvas(self):
        """Setup the drawing canvas."""
        self.canvas = CanvasWidget(self.class_names, self)
        self.layout.addWidget(self.canvas)

    def setupButtons(self):
        """Setup the buttons for canvas interaction."""
        button_layout = QHBoxLayout()

        self.setupButton("Clear", self.canvas.clear_canvas, button_layout)
        self.setupButton("Brush Size", self.showBrushSizeDialog, button_layout)
        self.setupButton("Undo", self.canvas.undo, button_layout)
        self.setupButton("Redo", self.canvas.redo, button_layout)
        self.setupButton("Predict", self.predictDrawing, button_layout)

        self.layout.addLayout(button_layout)

    def setupButton(self, text, on_clicked, layout):
        """Setup a button with the given text, clicked function, and layout."""
        button = QPushButton(text)
        button.clicked.connect(on_clicked)
        layout.addWidget(button)

    def showBrushSizeDialog(self):
        """Show dialog to set the brush size."""
        size, ok = QInputDialog.getInt(
            self, "Select Brush Size", "Size:", self.canvas.pen_width, 1, 50, 1
        )
        if ok:
            self.canvas.set_pen_width(size)

    def loadStylesheet(self):
        """Load and apply the stylesheet to the main window."""
        style_file = QFile("ui/resources/styles/stylesheet.qss")
        style_file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = bytes(style_file.readAll()).decode("utf-8")
        self.setStyleSheet(stylesheet)

    def predictDrawing(self):
        """Predict the drawing on the canvas."""
        drawing = self.canvas.get_drawing()

        if drawing is not None:
            img = self.qimageToPil(drawing).convert("RGB")
            img_resized = img.resize((45, 45))
            img_array = preprocess_image(img_resized)

            model = load_model("models/saved_models/trained_model.h5")
            prediction = model.predict(img_array)
            class_index = np.argmax(prediction)

            if class_index < len(self.class_names):
                class_name = self.class_names[class_index]
                confidence = prediction[0, class_index] * 100

                if confidence >= 60:
                    if confidence >= 90:
                        confidence_color = "green"
                    elif confidence >= 80:
                        confidence_color = "yellow"
                    else:
                        confidence_color = "red"

                    # Create the message with styled HTML text for prediction
                    message = f"<p><b>Predicted Class:</b> {class_name}</p>"
                    message += f"<p><b>Accuracy:</b> <font color='{confidence_color}'>{confidence:.2f}%</font></p>"

                    # Create QMessageBox with HTML content
                    msg_box = QMessageBox()
                    msg_box.setWindowTitle("Prediction")
                    msg_box.setTextFormat(Qt.RichText)
                    msg_box.setText(message)
                    msg_box.exec_()
                else:
                    # Low confidence warning message
                    warning_message = "The prediction confidence is too low to make a reliable prediction."

                    # Create QMessageBox for low confidence warning
                    msg_box = QMessageBox()
                    msg_box.setWindowTitle("Low Confidence Warning")
                    msg_box.setIcon(QMessageBox.Warning)
                    msg_box.setText(warning_message)
                    msg_box.setStandardButtons(QMessageBox.Ok)
                    msg_box.exec_()
            else:
                QMessageBox.warning(self, "Prediction", "Invalid class index")

    def qimageToPil(self, qimage):
        """Convert QImage to PIL Image."""
        width, height = qimage.width(), qimage.height()
        image_data = qimage.bits().asstring(width * height * 4)
        image = np.frombuffer(image_data, dtype=np.uint8).reshape((height, width, 4))
        image_pil = Image.fromarray(image)
        return image_pil
