from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QScrollArea,
    QFrame,
    QHBoxLayout,
    QPushButton,
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from utils.image_processing_utils import convert_pil_to_qimage


class PredictionResultWidget(QWidget):
    backClicked = pyqtSignal()  # Define a signal for the back button

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """Initialize the user interface."""
        self.layout = QVBoxLayout()
        self.scroll_area = QScrollArea()
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

        # Add a back button
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.onBackClicked)
        self.layout.addWidget(self.back_button)

        self.setLayout(self.layout)

    def onBackClicked(self):
        """Handle back button click event."""
        self.backClicked.emit()  # Emit the signal when the back button is clicked

    def addPrediction(self, class_name, confidence, image):
        """Add a new prediction result to the widget."""
        message = f"<p><b>Predicted Class:</b> {class_name}</p>"
        message += f"<p><b>Accuracy:</b> <font color='{self.getConfidenceColor(confidence)}'>{confidence:.2f}%</font></p>"

        # Create a horizontal layout for the image and message
        horizontal_layout = QHBoxLayout()

        # Convert the image to QPixmap and create an image label
        image_qt = convert_pil_to_qimage(image)  # Updated function call
        pixmap = QPixmap.fromImage(image_qt)
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setFixedWidth(pixmap.width())  # Set fixed width for consistency
        image_label.setFixedHeight(pixmap.height())  # Set fixed height for consistency

        # Create a label for the prediction text
        prediction_label = QLabel()
        prediction_label.setTextFormat(Qt.RichText)
        prediction_label.setText(message)
        prediction_label.setWordWrap(True)  # Allow text to wrap

        # Add the image and message labels to the horizontal layout
        horizontal_layout.addWidget(image_label)
        horizontal_layout.addWidget(prediction_label)

        # Add the horizontal layout to the scrollable layout
        self.scroll_layout.addLayout(horizontal_layout)

    def getConfidenceColor(self, confidence):
        """Return the color based on confidence level."""
        if confidence >= 80:
            return "green"
        elif confidence >= 60:
            return "yellow"
        else:
            return "red"
