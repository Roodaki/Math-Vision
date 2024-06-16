from PyQt5.QtGui import QPainter, QImage, QPen, QColor
from PyQt5.QtCore import Qt, QPoint, QRect, QSize
from PyQt5.QtWidgets import QWidget


class CanvasWidget(QWidget):
    def __init__(self, class_names, parent=None):
        super().__init__(parent)
        self.initUI()
        self.class_names = class_names

    def initUI(self):
        """Initialize the UI elements and attributes."""
        self.setAttribute(Qt.WA_StaticContents)
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)  # Initialize canvas with white color
        self.drawing = False  # Flag to indicate if drawing
        self.last_point = QPoint()  # Last drawn point
        self.pen_color = QColor(Qt.black)  # Default pen color
        self.pen_width = 5  # Default pen width
        self.undo_stack = []  # Stack to hold undo actions
        self.redo_stack = []  # Stack to hold redo actions

    def paintEvent(self, event):
        """Paint event handler."""
        canvas_painter = QPainter(self)
        canvas_painter.drawImage(self.rect(), self.image, self.image.rect())

    def resizeEvent(self, event):
        """Resize event handler to resize the canvas image."""
        if self.width() > self.image.width() or self.height() > self.image.height():
            new_width = max(self.width(), self.image.width())
            new_height = max(self.height(), self.image.height())
            self.resize_image(self.image, QSize(new_width, new_height))
            self.update()
        super().resizeEvent(event)

    def mousePressEvent(self, event):
        """Mouse press event handler."""
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = event.pos()

    def mouseMoveEvent(self, event):
        """Mouse move event handler."""
        if event.buttons() & Qt.LeftButton and self.drawing:
            self.draw_line_to(event.pos())

    def mouseReleaseEvent(self, event):
        """Mouse release event handler."""
        if event.button() == Qt.LeftButton:
            self.draw_line_to(event.pos())
            self.drawing = False
            self.save_snapshot()

    def draw_line_to(self, end_point):
        """Draw a line from the last point to the current point."""
        painter = QPainter(self.image)
        painter.setPen(
            QPen(
                self.pen_color, self.pen_width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin
            )
        )
        painter.drawLine(self.last_point, end_point)
        # Update the area where the line was drawn for optimization
        self.update(
            QRect(self.last_point, end_point)
            .normalized()
            .adjusted(-self.pen_width, -self.pen_width, self.pen_width, self.pen_width)
        )
        self.last_point = QPoint(end_point)

    def clear_canvas(self):
        """Clear the canvas (reset to white)."""
        self.image.fill(Qt.white)
        self.update()

    def resize_image(self, image, new_size):
        """Resize the image maintaining its content."""
        if image.size() == new_size:
            return
        new_image = QImage(new_size, QImage.Format_RGB32)
        new_image.fill(Qt.white)
        painter = QPainter(new_image)
        painter.drawImage(QPoint(0, 0), image)
        self.image = new_image

    def set_pen_color(self, color):
        """Set the pen color."""
        self.pen_color = color

    def set_pen_width(self, width):
        """Set the pen width."""
        self.pen_width = width

    def undo(self):
        """Undo the last drawing action."""
        if len(self.undo_stack) > 0:
            last_change = self.undo_stack.pop()
            self.redo_stack.append(self.image.copy())
            self.image = last_change
            self.update()

    def redo(self):
        """Redo the last undone drawing action."""
        if len(self.redo_stack) > 0:
            last_change = self.redo_stack.pop()
            self.undo_stack.append(self.image.copy())
            self.image = last_change
            self.update()

    def save_snapshot(self):
        """Save a snapshot of the current image for undo."""
        self.undo_stack.append(self.image.copy())
        self.redo_stack = []

    def get_drawing(self):
        """Get the current drawing."""
        return self.image
