from typing import Union

import jsons

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


def my_custom_datetime_serializer(obj: QPoint,
                                  **kwargs) -> [int, int]:
    return [obj.x(), obj.y()]

jsons.set_serializer(my_custom_datetime_serializer, QPoint)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

        self.verts = []
        self.mouse_pos = QPoint()
        self.snap = 20
        self.setMouseTracking(True)

    def initUI(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')

        saveAct = QAction('&Save as...', self)
        saveAct.setShortcut("Ctrl+S")
        saveAct.triggered.connect(self.saveAs)
        fileMenu.addAction(saveAct)

    def saveAs(self):
        name = QFileDialog.getSaveFileName(self, 'Save File')[0]

        f = open(name, 'w')

        with f:
            data = {"version": 1, "verts": self.verts}
            res = jsons.dumps(data)
            f.write(res)
            print("Saved data to {}!".format(name))

    def mouseMoveEvent(self, e):
        self.mouse_pos.setX(int(e.pos().x()/self.snap)*self.snap)
        self.mouse_pos.setY(int(e.pos().y()/self.snap)*self.snap)
        self.update()

    def mousePressEvent(self, e):
        self.verts.append(QPoint(self.mouse_pos))
        super().mousePressEvent(e)
        self.update()

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)

        painter.setBrush(Qt.lightGray)
        painter.setPen(Qt.darkGray)
        for region in range(int(0), int(len(self.verts)/int(3))):
            painter.drawPolygon(self.verts[region*3], self.verts[region*3+1], self.verts[region*3+2])

        painter.setPen(Qt.darkGreen)
        for vert in self.verts:
            painter.drawRect(vert.x()-1, vert.y()-1, 3, 3)

        painter.setPen(Qt.black)
        mx = self.mouse_pos.x()
        my = self.mouse_pos.y()
        painter.drawLine(mx, 0, mx, self.height)
        painter.drawLine(0, my, self.width, my)

app = QApplication([])
label = MainWindow()
label.width = 500
label.height = 500
label.show()
app.exec_()
