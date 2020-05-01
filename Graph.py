import random

"""глобальные переменные"""
RADIUS = 15     # радиус узлов
WIDTH, HEIGHT = 900, 600   # размеры поля


# узел графа
class Node:
    def __init__(self, label, x, y):
        self.label = label  # имя
        self.targets = []  # спиисок связей
        # координаты вершины
        self.x = x
        self.y = y

    def connect(self, node):  # соединение узлов
        if node not in self.targets:  # если такая связи не было
            self.targets.append(node)  # добавляем новую связь


class Graph:  # класс для представления графа
    def __init__(self):
        self.nodes = []  # список узлов
        self.size = 0  # количество вершин
        self.paths = []  # список простых путей

    def setSize(self, n):       # задает количество узлов графа и определет координаты каждого узла
        self.size = n
        # генерация узлов (присвоение имени и координат)
        for i in range(1, (n + 1)):
            x = random.randint(RADIUS * 4, WIDTH - RADIUS * 4 - 1)  # получаем случайные значения для координат
            y = random.randint(RADIUS * 4, HEIGHT - RADIUS * 4 - 1)
            new_node = Node(i, x, y)  # создаем узел графа
            self.nodes.append(new_node)  # добавляем в список узлов

    def addEdge(self, a, b):    # созать новую связь между узлами
        ind = a - 1  # от этого узла связь
        ind2 = b - 1    # связь к этому узлу
        self.nodes[ind].connect(self.nodes[ind2])  # добавляем связь

    # находит все возможные простые пути между двумя вершинами графа
    # рекурсивно. Затем записывает в paths
    def findPaths(self, a, b, path=None):
        if path == None:
            path = [a]
        for node in self.nodes[a - 1].targets:  # проходим по связям узла а
            m_path = [i for i in path]
            if node.label != b and node.label not in path:
                m_path.append(node.label)
                self.findPaths(node.label, b, m_path)
            elif node.label == b:
                m_path.append(node.label)
                self.paths.append(m_path)
