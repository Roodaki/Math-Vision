from PyQt5.QtGui import QPainter, QImage, QPen, QColor
from PyQt5.QtCore import Qt, QPoint, QRect, QSize
from PyQt5.QtWidgets import QWidget
from utils.constants import DEFAULT_SYMBOL_COLOR, DEFAULT_PADDING, DEFAULT_PEN_WIDTH
from utils.symbol_segmentation_utils import find_all_symbols_bounding_boxes


class CanvasWidget(QWidget):
    def __init__(self, class_names, parent=None):
        super().__init__(parent)
        self.initializeCanvasWidget(class_names)

    def initializeCanvasWidget(self, class_names):
        """Initialize the canvas widget."""
        self.class_names = class_names
        self.bounding_boxes = []
        self.symbol_color = DEFAULT_SYMBOL_COLOR  # Default symbol color
        self.padding = DEFAULT_PADDING  # Default padding
        self.setupDrawingParameters()

    def setupDrawingParameters(self):
        """Setup initial drawing parameters and attributes."""
        self.setAttribute(Qt.WA_StaticContents)
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.drawing = False
        self.last_point = QPoint()
        self.pen_color = QColor(Qt.black)
        self.pen_width = DEFAULT_PEN_WIDTH
        self.undo_stack = []
        self.redo_stack = []

    def paintEvent(self, event):
        """Handle paint event to draw the canvas and bounding boxes."""
        canvas_painter = QPainter(self)
        canvas_painter.drawImage(self.rect(), self.image, self.image.rect())
        if self.bounding_boxes:
            self.drawBoundingBoxes(canvas_painter)

    def drawBoundingBoxes(self, painter):
        """Draw bounding boxes on the canvas."""
        pen = QPen(Qt.red, 2, Qt.SolidLine)
        painter.setPen(pen)
        for box in self.bounding_boxes:
            x_min, y_min, x_max, y_max = box
            painter.drawRect(x_min, y_min, x_max - x_min, y_max - y_min)

    def resizeEvent(self, event):
        """Handle resize event to adjust the image size."""
        if self.width() > self.image.width() or self.height() > self.image.height():
            new_width = max(self.width(), self.image.width())
            new_height = max(self.height(), self.image.height())
            self.resizeImage(self.image, QSize(new_width, new_height))
            self.update()
        super().resizeEvent(event)

    def mousePressEvent(self, event):
        """Handle mouse press event to start drawing."""
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = event.pos()

    def mouseMoveEvent(self, event):
        """Handle mouse move event to draw lines."""
        if event.buttons() & Qt.LeftButton and self.drawing:
            self.drawLineTo(event.pos())

    def mouseReleaseEvent(self, event):
        """Handle mouse release event to finish drawing."""
        if event.button() == Qt.LeftButton:
            self.drawLineTo(event.pos())
            self.drawing = False
            self.saveCanvasSnapshot()
            self.updateBoundingBoxes()

    def drawLineTo(self, end_point):
        """Draw a line from the last point to the current end point."""
        painter = QPainter(self.image)
        painter.setPen(
            QPen(
                self.pen_color, self.pen_width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin
            )
        )
        painter.drawLine(self.last_point, end_point)
        self.update(
            QRect(self.last_point, end_point)
            .normalized()
            .adjusted(-self.pen_width, -self.pen_width, self.pen_width, self.pen_width)
        )
        self.last_point = QPoint(end_point)

    def clearCanvas(self):
        """Clear the canvas."""
        self.image.fill(Qt.white)
        self.bounding_boxes = []
        self.update()

    def resizeImage(self, image, new_size):
        """Resize the image to the new size."""
        if image.size() == new_size:
            return
        new_image = QImage(new_size, QImage.Format_RGB32)
        new_image.fill(Qt.white)
        painter = QPainter(new_image)
        painter.drawImage(QPoint(0, 0), image)
        self.image = new_image

    def setPenColor(self, color):
        """Set the pen color for drawing."""
        self.pen_color = color
        self.symbol_color = color  # Update symbol color

    def setPenWidth(self, width):
        """Set the pen width for drawing."""
        self.pen_width = width

    def undoDrawing(self):
        """Undo the last drawing action."""
        if len(self.undo_stack) > 0:
            last_change = self.undo_stack.pop()
            self.redo_stack.append(self.image.copy())
            self.image = last_change
            self.updateBoundingBoxes()
            self.update()

    def redoDrawing(self):
        """Redo the last undone drawing action."""
        if len(self.redo_stack) > 0:
            next_change = self.redo_stack.pop()
            self.undo_stack.append(self.image.copy())
            self.image = next_change
            self.updateBoundingBoxes()
            self.update()

    def saveCanvasSnapshot(self):
        """Save a snapshot of the current canvas state for undo/redo."""
        self.undo_stack.append(self.image.copy())
        self.redo_stack.clear()

    def updateBoundingBoxes(self):
        """Update bounding boxes for the current drawing."""
        self.bounding_boxes = find_all_symbols_bounding_boxes(
            self.image,
            (
                self.symbol_color.red(),
                self.symbol_color.green(),
                self.symbol_color.blue(),
            ),
            self.padding,
        )
        self.update()

    def getDrawing(self):
        """Get the current drawing as a QImage."""
        return self.image
