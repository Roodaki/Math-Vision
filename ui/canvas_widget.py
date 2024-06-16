from PyQt5.QtGui import QPainter, QImage, QPen, QColor
from PyQt5.QtCore import Qt, QPoint, QSize, QRect
from PyQt5.QtWidgets import QWidget

class CanvasWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StaticContents)
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.drawing = False
        self.last_point = QPoint()
        self.pen_color = QColor(Qt.black)
        self.pen_width = 5

        self.undo_stack = []
        self.redo_stack = []

    def paintEvent(self, event):
        canvas_painter = QPainter(self)
        canvas_painter.drawImage(self.rect(), self.image, self.image.rect())

    def resizeEvent(self, event):
        if self.width() > self.image.width() or self.height() > self.image.height():
            new_width = max(self.width(), self.image.width())
            new_height = max(self.height(), self.image.height())
            self.resize_image(self.image, QSize(new_width, new_height))
            self.update()

        super().resizeEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.drawing:
            self.draw_line_to(event.pos())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.draw_line_to(event.pos())
            self.drawing = False
            self.save_snapshot()

    def draw_line_to(self, end_point):
        painter = QPainter(self.image)
        painter.setPen(QPen(self.pen_color, self.pen_width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(self.last_point, end_point)
        self.update(QRect(self.last_point, end_point).normalized().adjusted(-self.pen_width, -self.pen_width, self.pen_width, self.pen_width))
        self.last_point = QPoint(end_point)

    def clear_canvas(self):
        self.image.fill(Qt.white)
        self.update()

    def resize_image(self, image, new_size):
        if image.size() == new_size:
            return

        new_image = QImage(new_size, QImage.Format_RGB32)
        new_image.fill(Qt.white)
        painter = QPainter(new_image)
        painter.drawImage(QPoint(0, 0), image)
        self.image = new_image

    def set_pen_color(self, color):
        self.pen_color = color

    def set_pen_width(self, width):
        self.pen_width = width

    def undo(self):
        if len(self.undo_stack) > 0:
            last_change = self.undo_stack.pop()
            self.redo_stack.append(self.image.copy())
            self.image = last_change
            self.update()

    def redo(self):
        if len(self.redo_stack) > 0:
            last_change = self.redo_stack.pop()
            self.undo_stack.append(self.image.copy())
            self.image = last_change
            self.update()

    def save_snapshot(self):
        self.undo_stack.append(self.image.copy())
        self.redo_stack = []

