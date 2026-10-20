from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
import numpy as np

from fonction import Fonction
from fonction_derivee import FonctionDerivee

class Canvas(FigureCanvasQTAgg):

    __fig1 : plt.subplots
    __fig2 : plt.subplots
    __ax1 : plt.subplots
    __ax2: plt.subplots
    __model : Fonction
    __model_derivee : FonctionDerivee

    def __init__(self, model : Fonction, model_derivee : FonctionDerivee):
        # création d'une figure matplotlib
        self.__fig1, self.__ax1 = plt.subplots()
        self.__fig2, self.__ax2 = plt.subplots()

        # appel du constructeur parent avec les figs en parametre
        super().__init__(self.__fig1, self.__fig2)

        # garder la reférence sur le model
        self.__model = model
        self.__model_derivee = model_derivee

    def dessiner(self):                                          #####         À ne pas oublier: Faire dessiner la dérivé
            self.__ax1.clear()  # Efface les anciens axes
            self.__ax2.clear()

            # 3. Génération des points x pour l'évaluation
            if self.__model.fonction:
                x1 = np.linspace(self.__Xmin, self.__Xmax, 500)
                y1 = self.__model.fonction(x1)

                x2 = np.linspace(self.__Xmin, self.__Xmax, 500)
                y2 = self.__model.fonctionDerivee(x2)

                # Gestion du cas où f(x) est une constante
                if isinstance(y1, (int, float, np.number)):
                    y = np.full_like(x1, y1)

                self.__ax1.plot(x1, y1, color=self.__model.couleur)
                self.__ax2.plot(x2, y2, color=self.__modelDerivee.couleurDerivee)


            # Configuration des options visuelles (titre)
            self.__ax1.plot(self.__model.couleur)
            self.__ax2.plot(self.__modelDerivee.couleurDerivee)

            self.__ax1.set_title("Fonction originale")
            self.__ax2.set_title("Fonction derivée")

            # Rafraîchissement du canvas Qt
            self.draw()