from Form import *

# окно приложения
window = Tk()
window.geometry("1200x900")
window.title("Сиаод, 3 лабораторная, Литвненко Борис ИКБО-06-18")
g = Graph()     # граф с которым производятся действия
w = Form(window, g)     # создаю форму и указываю с каким графом надо работать
window.mainloop()