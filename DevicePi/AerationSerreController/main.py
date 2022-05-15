import tkinter as tk

from Controllers.AerationController import AerationController as AerationController
from Models.AerationModel import AerationModel
from Views.MainWindow import MainWindow


class Main(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Contrôle d’une porte d’aération d’une serre')

        # Model
        model = AerationModel()

        # View
        view = MainWindow(self)

        # Controller
        controller = AerationController(model, view, 'automatic')

        view.set_controller(controller)


if __name__ == '__main__':
    app = Main()
    app.mainloop()
