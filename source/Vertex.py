from PyQt6 import QtWidgets
from PyQt6.QtGui import QColor, QPen
from PyQt6.QtWidgets import QGraphicsItem

class Vertex(QtWidgets.QGraphicsEllipseItem):
    """клас який представляє вершину"""

    def __init__ (self,x,y):
        super().__init__(0, 0, 26, 26)


        self.setX(x)
        self.setY(y)
        self.setPen(QPen(QColor('black'),3))
        self.setBrush( QColor(127, 90, 255))        
        self.setZValue(2)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)

        self.edges = []

    def __eq__(self, vert):
        if self.x() == vert.x() and self.y() == vert.y():
            return True
        else:
            return False

    def __str__(self):
        return '('+str(self.x()) +';'+ str(self.y()) +')'

    def __hash__(self):
        return hash((self.x(), self.y()))
