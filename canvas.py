from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
import numpy as np

from fonction import Fonction


class Canvas(FigureCanvasQTAgg):

    __fig : plt.subplots
    __ax : plt.subplots
    __model : Fonction

    def __init__(self, model : Fonction):
        # création d'une figure matplotlib
        self.__fig, self.__ax = plt.subplots()

        # appel du constructeur parent avec la fig en parametre
        super().__init__(self.__fig)

        # garder la reférence sur le model
        self.__model = model

    def dessiner(self):
        pass