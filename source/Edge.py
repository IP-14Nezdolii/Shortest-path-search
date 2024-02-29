from PyQt6 import QtWidgets
from PyQt6.QtGui import QColor, QPen
from PyQt6.QtWidgets import QGraphicsItem

class Edge(QtWidgets.QGraphicsLineItem):
    """клас який представляє ребро"""

    def __init__ (self, vert1,vert2, val = 0):
        super().__init__(vert1.x()+13, vert1.y()+13, vert2.x() + 13, vert2.y() + 13)
        self.setZValue(1)
        self.setPen(QPen(QColor(128,128,255),3))
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)

        vert1.edges.append(self)
        vert2.edges.append(self)

        self.vertices = [vert1, vert2]
        self.vertices.sort(key = lambda vert: (vert.x(), vert.y()))

        self.value = val

    def __eq__(self, edge):
        if self.vertices == edge.vertices:
            return True
        else:
            return False

    def __str__(self):
        return '('+'('+str(self.vertices[0]) +','+ str(self.vertices[1])+')'+str( self.value)+')'

    def __hash__(self):
        return hash((self.vertices[0].x(), self.vertices[0].y(), self.vertices[1].x(), self.vertices[1].y()))
