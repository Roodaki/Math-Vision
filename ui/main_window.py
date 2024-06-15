from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QColorDialog, QInputDialog
from PyQt5.QtGui import QColor
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

        self.color_button = QPushButton("Select Color")
        self.color_button.clicked.connect(self.show_color_dialog)
        self.layout.addWidget(self.color_button)

        self.brush_size_button = QPushButton("Brush Size")
        self.brush_size_button.clicked.connect(self.show_brush_size_dialog)
        self.layout.addWidget(self.brush_size_button)

    def show_color_dialog(self):
        color = QColorDialog.getColor(initial=self.canvas.pen_color)
        if color.isValid():
            self.canvas.set_pen_color(color)

    def show_brush_size_dialog(self):
        size, ok = QInputDialog.getInt(self, "Select Brush Size", "Size:", self.canvas.pen_width, 1, 50, 1)
        if ok:
            self.canvas.set_pen_width(size)
