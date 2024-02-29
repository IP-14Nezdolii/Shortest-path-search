from PyQt6 import QtWidgets , QtCore, QtGui
from PyQt6.QtGui import QColor, QPen
from PyQt6.QtWidgets import QGraphicsItem, QGraphicsRectItem

from Vertex import Vertex
from Edge import Edge

class Graph:
    """клас який представляє граф"""

    def __init__(self):
        self.vert_lst = []
        self.__edge_lst = []
        self.min_span_tree = []

    def add_vert(self, vert):
        """додає вершину в граф"""
        self.vert_lst.append(vert)

    def add_edge(self, edge):
        """додає ребро в граф"""
        self.__edge_lst.append(edge)

    def clear_graph(self):
        """очищає граф"""
        self.vert_lst.clear()
        self.__edge_lst.clear()
        self.min_span_tree.clear()

    def vert_is_distanced(self, coord_x, coord_y):
        """перевіряє чи знаходиться вершина на певній відстані від інших"""
        dist = lambda x,y: (((coord_x - x)**2 + (coord_y - y)**2)**(0.5))
        for vert in self.vert_lst:
            if dist(vert.x(), vert.y()) < 55:
                return False
        return True

    def edge_in_graph(self, edge):
        """перевіряє на наявність ребра в графі"""
        return edge in self.__edge_lst

    def all_vertices_are_connected(self):
        """перевіряє чи з'єднані всі вершини"""
        if len(self.vert_lst) == 0:
            return False
        for vert in self.vert_lst:
            if len(vert.edges) == 0:
                return False
        return True

    def all_edges_have_val(self):
        """перевіряє на наявніст ваги у кожного ребра"""
        if len(self.__edge_lst) == 0:
            return False
        for edge in self.__edge_lst:
            if edge.value == 0:
                return False
        return True

    def graph_is_connected(self):
        """перевіряє граф на зв'язність"""
        if len(self.__edge_lst) < len(self.vert_lst) - 1:
            return False

        vert_set = set()    # множина вершин
        edge_set = set()    # множина ребер
        vert_set.update(set(self.__edge_lst[0].vertices))
        edge_set.add( self.__edge_lst[0])
                
        # зі списку ребер додається ребро, щоб одна з його вершин належить множині вершин, а інша — ні.
        prev_ln = 0
        while len(edge_set) != prev_ln and len(edge_set) != len(self.__edge_lst):
            prev_ln = len(edge_set)
            for edge in self.__edge_lst:
                if vert_set.isdisjoint(set(edge.vertices)) == False:
                    vert_set.update(set(edge.vertices))
                    edge_set.add(edge)

        if len(edge_set) == len(self.__edge_lst):
            return True
        else:
            return False

    def graph_was_built(self):
        """перевіряє граф на коректну побудову"""
        if self.all_vertices_are_connected() == True:
            if self.all_edges_have_val() == True:
                if self.graph_is_connected() == True:
                    return True
        return False

    def Kruskals_alg(self):
        """алгоитм Крускала"""
        self.__edge_lst.sort(key = lambda x: x.value)

        vert_dict = {}  #словник вершин
       
        for edge in self.__edge_lst:
            p = edge.vertices.copy()

            if p[0] not in vert_dict or p[1] not in vert_dict:  # якщо ребро не утворює цикл
                if p[0] not in vert_dict and p[1] not in vert_dict: # якщо дві вершини не з'єднані
                    vert_dict[p[0]] = [p[0], p[1]]
                    vert_dict[p[1]] = vert_dict[p[0]]
                else:   # якщо в словнику немає одної з вершин                                             
                    if not vert_dict.get(p[0]):
                        vert_dict[p[1]].append(p[0])            
                        vert_dict[p[0]] = vert_dict[p[1]]          
                    else:
                        vert_dict[p[0]].append(p[1])               
                        vert_dict[p[1]] = vert_dict[p[0]]

                self.min_span_tree.append(edge)                                 

        for edge in self.__edge_lst:  # об'єднує вершини з різних груп
            p = [edge.vertices[0], edge.vertices[1]]

            if p[1] not in vert_dict[p[0]]:
                self.min_span_tree.append(edge)                                
                lst = vert_dict[p[0]]
                vert_dict[p[0]] += vert_dict[p[1]]                  
                vert_dict[p[1]] += lst

    def Boruvkas_alg(self):
        """алгоитм Борувки"""
        comp_lst = [set([vert]) for vert in self.vert_lst]  # список компонент зв'язності         
        e_lst = []   # список ребер

        for vert in self.vert_lst:
            vert.edges.sort(key=lambda x: x.value)

        while len(e_lst) < len(self.vert_lst) - 1:

            # для кожної компоненти зв'язності знаходе найдешевше ребро, що пов'язує цю компоненту з будь-якою іншою
            for vert_set in comp_lst:
                min_edge = None     # ребро з найменшою вагою
                for vert in vert_set:
                    for edge in vert.edges:
                        if (vert_set >= set(edge.vertices)) == False:    # якщо ребро об'єднує одну компоненту зв'язності з будь-якою іншою
                            if min_edge is None:
                                min_edge = edge
                            elif edge.value < min_edge.value:
                                min_edge = edge
                            elif edge.value == min_edge.value and edge in e_lst:
                                min_edge = edge
                                break
                            elif edge.value > min_edge.value:
                                break
                if min_edge is not None:
                    if min_edge not in e_lst:
                        e_lst.append(min_edge)
                    vert_set.add(min_edge.vertices[0])
                    vert_set.add(min_edge.vertices[1])

            # об'єднує компоненти зв'язності зі спільними вершинами
            i = 0
            while i < len(comp_lst):
                j = i+1
                while j < len(comp_lst):
                    if comp_lst[i].isdisjoint(comp_lst[j]) == False:
                        comp_lst[i].update(comp_lst[j])
                        comp_lst.pop(j)
                        j -= 1
                    j += 1
                i += 1

        self.min_span_tree = e_lst.copy()

    def Prims_alg(self):
        """алгоитм Прима"""
        self.__edge_lst.sort(key=lambda x: x.value)

        vert_set = set()    # множина вершин

        vert_set.update(set(self.__edge_lst[0].vertices))
        self.min_span_tree.append(self.__edge_lst[0])

        # на кожній ітерації знаходе найдешевше ребро, що одна з його вершин належить дереву, а інша — ні.
        while len(vert_set) != len(self.vert_lst):  
            for edge in self.__edge_lst:
                points_set = set(edge.vertices)
                if ((vert_set >= points_set) == False) and (vert_set.isdisjoint(points_set) == False):
                    vert_set.update(points_set)
                    self.min_span_tree.append(edge)
                    break           

    def weight_of_tree(self):
        """повертає вагу остовного дерева мінімальної ваги"""
        weight = 0
        for edge in self.min_span_tree:
            weight += edge.value
        return weight

    def save_graph(self, fileName):
        """зберігає граф у текстовий файл"""
        outFile = open(fileName,'w')

        outFile.write('edge_lst:' + '\n')
        for edge in self.__edge_lst:
            outFile.write(str(edge) + '\n')

        outFile.write('min_span_tree:' + '\n')
        for edge in self.min_span_tree:
            outFile.write(str(edge) + '\n')            

        outFile.close()

