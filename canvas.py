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
            self.__ax.clear()  # Efface les anciens axes

            # 3. Génération des points x pour l'évaluation
            if self.__model.fonction:
                x = np.linspace(-10, 10, 500)
                y = self.__model.fonction(x)

                # Gestion du cas où f(x) est une constante
                if isinstance(y, (int, float, np.number)):
                    y = np.full_like(x, y)

                self.__ax.plot(x, y, color=self.__model.couleur)

            # # Configuration des options visuelles (grille et titre)
            # self.__ax.grid(self.__model.showGrille)
            # if self.__model.titre:
            #     self.__ax.set_title(self.__model.titre)

            # Rafraîchissement du canvas Qt
            self.draw()