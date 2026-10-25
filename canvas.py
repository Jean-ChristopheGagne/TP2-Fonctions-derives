from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
import numpy as np

from fonction import Fonction

class Canvas(FigureCanvasQTAgg):

    __fig : plt.Figure
    __model : Fonction

    def __init__(self, model : Fonction):
        # création d'une figure matplotlib
        self.__fig, self.__ax = plt.subplots(1,2)

        # appel du constructeur parent avec la fig en parametre
        super().__init__(self.__fig)

        # garder la reférence sur le model
        self.__model = model
        self.dessiner()

    def dessiner(self):
            print("toto")
            self.__ax[0].clear()
            self.__ax[1].clear()                                   # Efface les anciens axes

            # 3. Génération des points x pour l'évaluation
            if self.__model.fonction:
                x = np.linspace(self.__model.x_min, self.__model.x_max, 500)
                y = self.__model.fonction(x)

                # Gestion du cas où f(x) est une constante
                if isinstance(y, (int, float, np.number)):
                    y = np.full_like(x, y)

                self.__ax[0].plot(x, y, color=self.__model.couleur)
                self.__ax[1].plot(x, y, color=self.__model.couleur)


            # Configuration des options visuelles(couleurs)
            # self.__ax[0].plot(self.__model.couleur)
            # self.__ax[1].plot(self.__model.couleur)

            # Configuration des titres
            self.__ax[0].set_title("Fonction originale")
            self.__ax[1].set_title("Fonction dérivée")

            #Affichage de la grille
            self.__ax[0].grid(True)
            self.__ax[1].grid(True)

            # Rafraîchissement du canvas Qt
            self.draw()