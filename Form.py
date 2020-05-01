# импортируем необходимые библиотеки
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
from Graph import *


class Form():
    def __init__(self, root, graph):  # root - форма размещения, graph - граф для работы
        self.canvas = \
            Canvas(root, width=WIDTH, height=HEIGHT, background="White")  # "холст" рисования графа

        self.frame = Frame(root)  # рамка для размещения объектов добавления данных
        self.buttonNew = Button(self.frame, text="Создать", command=self.initialize)    # кнопка добавления количества вершин графа
        self.buttonFile = Button(self.frame, text="Взять из матрицы", command=self.initializeFile)  # по нажатии берется матрица из файла мatrix.txt
        self.button2 = Button(self.frame, text="Добавить", command=self.add_edge)   # кнопка добавления связи между графами
        self.buttonCount = Button(root, text="Нати наибольший простой путь (пути)", command=self.count)  # Начать задание
        self.label = Label(self.frame, text="Количество вершин будущего графа")     # информационный label
        self.label.pack(side=LEFT)  # показываем информационный label
        self.nEntry = StringVar()  # для чтения из текстового поля
        self.lineEdit = Entry(self.frame, textvariable=self.nEntry)  # поле для ввода
        self.lineEdit.pack(side=LEFT, padx=10, pady=10)  # размещаем поле и задаем пространство между виджетами
        self.buttonNew.pack(side=LEFT, padx=10, pady=10)    # размещаем кнопку и задаем пространство между виджетами
        self.buttonFile.pack(side=LEFT, padx=10, pady=10)   # размещаем кнопку и задаем пространство между виджетами

        self.frame.pack()
        self.labelResult = Label(root, text="")  # поле вывода ответа
        self.canvas.pack(side=BOTTOM)  # добавляем на рамку поле для рисования
        self.buttonCount.pack(side=BOTTOM)
        self.labelResult.pack(side=BOTTOM)
        self.graph = graph

    def initialize(self):
        try:
            self.n = int(self.lineEdit.get())
            if self.n <= 0:
                raise ValueError
            self.label["text"] = "Добавить ребро (пример: 1-2)"
            self.graph.setSize(self.n)  # устанавливаем размер графа
            self.buttonNew.pack_forget()  # убираем кнопку
            self.buttonFile.pack_forget()  # и эту
            self.button2.pack(side=LEFT)
            self.lineEdit.delete(0, END)  # очищаем поле ввода
            self.draw()
        except ValueError:
            messagebox.showinfo('Ошибка', 'Проверьте правильность заполнения поля')

    def initializeFile(self):
        try:
            # в файле граф представлен в виде матрицы смежности
            with open('matrix.txt', 'r') as f:
                matrix = f.read().splitlines()
            self.len = len(matrix)  # сторона матрицы
            self.graph.setSize(self.len)  # устанавливаем размер графа
            # добавляем все связи
            for n_line in range(self.len):
                for n_char in range(self.len):
                    if matrix[n_line][n_char] == "1":
                        self.graph.addEdge(n_line+1, n_char+1)
            self.draw()  # отрисовываем граф
            self.buttonNew.pack_forget()     # убираем кнопку
            self.buttonFile.pack_forget()    # и эту
            self.button2.pack(side=LEFT)    # и ставим нужную, что б можно было дополнить граф
            self.label["text"] = "Добавить ребро (пример: 1-2)"
        except FileNotFoundError:
            messagebox.showinfo('Ошибка', 'Ошибка открытия файла')
        except Exception:
            messagebox.showinfo('Ошибка', 'Ошибка при заполнении')

    def add_edge(self):
        line = self.lineEdit.get()
        self.n = self.graph.size
        try:
            line.split(",")
            for l in line:
                a = int(line.split('-')[0])  # разбиваем введенную строку на два числа
                b = int(line.split('-')[1])
            self.lineEdit.delete(0, END)  # очищаем поле ввода
            if (a < 1 or b < 1 or a > self.n or b > self.n or a == b):  # если номер ребра неправильный
                messagebox.showinfo('Ошибка', 'Некорректные значения')
                return
            self.graph.addEdge(a, b)    # добавляем новую связь
            self.draw()  # рисуем заново граф со связями
        except Exception:
            messagebox.showinfo('Ошибка', 'Проверьте правильность заполнения полей - две цифры через тире (1-2)')

    # красиво записывает список в строку [1, 2, 3] -> "1 2 3"
    def str_p(self, path):
        res = ""
        for n in path:
            res += (str(n) + " ")
        return res

    # выполняет задание
    def count(self):
        self.graph.paths = []   # обнуляем все пути на случай, если задание выполняется повторно
        # перебирает все возможные сочетания вершин "от до",
        # находит все возможные простые пути между каждо парой вершин и
        # и записывает в paths
        for i in range(len(self.graph.nodes)):
            for j in range(len(self.graph.nodes)):
                if i == j:
                    continue
                self.graph.findPaths(i + 1, j + 1)
        # вывод ответа на задание
        l_max = 0    # максимальная длина
        result = ""  # итоговый результат
        for path in self.graph.paths:
            if len(path) > l_max:
                l_max = len(path)
                result = self.str_p(path)
            elif len(path) == l_max:
                result += ('\n' + self.str_p(path))
        result = "Ответ: максимальная длина -  " + str(l_max) + ", у простого путя (путей): \n" + result
        self.labelResult["text"] = result

    """следующие методы для открисовки графа"""
    def draw_node(self, x, y, text, r=RADIUS):
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="MistyRose")  # рисуем узлы
        self.canvas.create_text(x, y, text=text)  # добавляем подписи

    def draw_graph(self):
        for s in self.graph.nodes:  # проходим по списку узлов
            for t in s.targets:  # проходим по списку его соседей
                self.canvas.create_line(s.x, s.y, t.x, t.y, width=2, arrow=LAST,
                                        arrowshape="15 50 15")  # отрисовываем линию соединяющую вершины
        for n in self.graph.nodes:
            self.draw_node(n.x, n.y, n.label)  # отрисовываем узел

    def draw(self):
        self.canvas.delete("all")  # очищаем рисунок
        self.draw_graph()  # рисуем заново
