from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton
from canvas.canvas_widget import CanvasWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Professional Paint App")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.canvas = CanvasWidget(self)
        self.layout.addWidget(self.canvas)

        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.canvas.clear_canvas)
        self.layout.addWidget(self.clear_button)
