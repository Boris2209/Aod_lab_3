from Form import *

# окно приложения
window = Tk()
window.geometry("1200x900")
window.title("Graph")
g = Graph()     # граф с которым производятся действия
w = Form(window, g)     # создаю форму и указываю с каким графом надо работать
window.mainloop()