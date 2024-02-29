from PyQt6 import QtWidgets , QtCore, QtGui
from PyQt6.QtGui import QColor, QPen
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsItem, QGraphicsRectItem
from Graph import Graph, Vertex, Edge
from Ui import Ui
import time


class MainWindow(QMainWindow):
    """клас який представляє головне вікно"""

    def __init__(self):
        super(MainWindow, self).__init__()

        self.resize(1015, 700)

        self.__ui = Ui()
        self.__ui.setupUi(self)

        self.setWindowTitle("My App")

        self.__scene = QtWidgets.QGraphicsScene()                         
        self.__scene.setSceneRect(30, 100, 985, 535)

        self.__view = QtWidgets.QGraphicsView(self.__scene, self)
        self.__view.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        self.__view.setGeometry(10,75,1000,560)
        
        self.__graph = Graph()

        self.__prev_vert = None   # буферна змінна для побудови ребра                                       
        self.__scene.selectionChanged.connect(self.select_vert)

        self.__ui.pushButton.clicked.connect(self.btn_was_clicked)    # кнопка Обрахувати
        self.__ui.pushButton_2.clicked.connect(self.btn2_was_clicked) # кнопка Зберегти
        self.__ui.pushButton_3.clicked.connect(self.clear_graph)      # кнопка Видалити граф
        self.__ui.pushButton_4.clicked.connect(self.btn4_was_clicked) # кнопка Задати
        
        self.__ui.lineEdit.setPlaceholderText("Введіть вагу")

        self.__ui.radioButton_3.toggled.connect(self.radio_btn_toggled)
    
    def radio_btn_toggled(self):
        """керує доступом до віджетів для встановлення ваги ребра"""
        if self.__ui.radioButton_3.isChecked() == True:
            self.__ui.pushButton_4.setEnabled(True)
            self.__ui.lineEdit.setEnabled(True)
        else:
            self.__ui.pushButton_4.setEnabled(False)
            self.__ui.lineEdit.setEnabled(False)
        

    def  mousePressEvent(self, event):
        """викликає метод створення вершини"""
        if self.__ui.radioButton.isChecked() == True:
            if event.button() == Qt.MouseButton.LeftButton:
                self.add_vert(event.pos().x(), event.pos().y())

    def add_vert(self,  x, y):
        """додає вершину в граф та сцену"""
        if x > 30 and y > 90 and x < 985 and y < 610:
            if self.__graph.vert_is_distanced(x, y) == True:
                vert = Vertex(x,y)
                self.__graph.add_vert(vert)


                text = QtWidgets.QGraphicsSimpleTextItem(str(len(self.__graph.vert_lst)))
                text.setPen(QPen(QColor('black'),1))
                text.setZValue(3)
                text.setX(x+7)
                text.setY(y+2)
                text.setFont(QtGui.QFont("MS",15))                    
                self.__scene.addItem(text)


                self.__scene.addItem(vert)
    
    def btn_was_clicked(self):
        """викликає відповідний метод знаходження остовного дерева, відповідно до вибору користувача в comboBox"""
        if self.__graph.graph_was_built() == True:
            alg = self.__ui.comboBox.currentText()
            if alg == "Алгоритм Прима":
                self.__graph.Prims_alg()
                self.__ui.textBrowser.append('Kістякове дерево побудовано алгоритмом Прима.')
            elif alg == "Алгоритм Крускала":
                self.__graph.Kruskals_alg()
                self.__ui.textBrowser.append('Kістякове дерево побудовано алгоритмом Крускала.')
            elif alg == "Алгоритм Борувки":                
                self.__graph.Boruvkas_alg()
                self.__ui.textBrowser.append('Kістякове дерево побудовано алгоритмом Борувки.')
            self.enabled(False)
            self.__ui.pushButton_3.setEnabled(False)
            self.paint_tree()
            self.__ui.pushButton_3.setEnabled(True)
            self.__ui.textBrowser.append('Вага остовного дерева мінімальної ваги: ' + str(self.__graph.weight_of_tree()) + '.')
        else:
            self.__ui.textBrowser.append('Граф побудовано некоректно!')

    def btn2_was_clicked(self):
        """викликає метод запису результатів роботи у текстовий файл"""
        if len(self.__graph.min_span_tree) != 0:
            self.__graph.save_graph('AppFile.txt')
            self.__ui.textBrowser.append('Результат було збережено.')
        else:
            self.__ui.textBrowser.append('Остовне дерево не побудовано.')

    def btn4_was_clicked(self):
        """зчитує рядок з lineEdit, конвертує його в float та викликає метод, що додає вагу вибраним ребрам"""
        try: 
            val = float(self.__ui.lineEdit.text())
        except: 
            self.__ui.lineEdit.clear()
            self.__ui.textBrowser.append('Введено некоректні значення!')
            return
        if val > 0 and val < float('inf'):
            self.add_value_to_edge(val)
        else:           
            self.__ui.textBrowser.append('Введено некоректні значення!')
        self.__ui.lineEdit.clear()

    def select_vert(self):
        """керує вибором двох вершини для створення ребра"""
        if self.__ui.radioButton_2.isChecked() == True:
            try:
                items = self.__scene.selectedItems()    
            except: 
                return

            if len(items) == 0:
                self.__prev_vert = None 
                return   
             
            if len(items) == 1:
                if type(items[0]) is Vertex:
                    if self.__prev_vert is not None:                   
                        self.add_edge(items[0],self.__prev_vert)
                        self.__prev_vert = None
                    else:
                        self.__prev_vert = items[0]

    def add_value_to_edge(self,val):
        """задає вагу вибраним ребрам"""
        items = self.__scene.selectedItems()
        for item in items:
            if type(item) is Edge:
                if item.value == 0:                  
                    item.value = val

                    text = QtWidgets.QGraphicsSimpleTextItem(str(val))
                    text.setPen(QPen(QColor('black'),1))
                    text.setZValue(3)
                    text.setX((item.vertices[0].x() + item.vertices[1].x())/2)
                    text.setY((item.vertices[0].y() + item.vertices[1].y())/2)
                    text.setFont(QtGui.QFont("MS",15))                    
                    self.__scene.addItem(text)

    def add_edge(self, vert1, vert2):
        """додає ребро"""
        if vert1 != vert2:
            edge = Edge(vert1,vert2)
            if self.__graph.edge_in_graph(edge) == False:
                self.__scene.addItem(edge)
                self.__graph.add_edge(edge)

    def clear_graph(self):
        """очищає граф та поле"""
        self.__prev_vert = None
        self.__graph.clear_graph()               
        self.__scene.clear()
        self.enabled(True)

    def enabled(self,en): 
        """керує доступом до віджетів для побудови графа"""
        self.__ui.comboBox.setEnabled(en)

        self.__ui.radioButton.setEnabled(en)
        self.__ui.radioButton_2.setEnabled(en)
        self.__ui.radioButton_3.setEnabled(en)
        self.__ui.radioButton_3.setChecked(True)

        self.__ui.lineEdit.setEnabled(en)

        self.__ui.pushButton.setEnabled(en)
        self.__ui.pushButton_4.setEnabled(en)

    def paint_tree(self):
        """розфарбовує остовне дерево мінімальної ваги в порядку додання ребер до остова"""       
        for edge in self.__graph.min_span_tree:
            edge.setPen(QPen(QColor (255,0,127),3))
            QApplication.processEvents()
            time.sleep(1.5)
            
        
            

        
        
        
        
