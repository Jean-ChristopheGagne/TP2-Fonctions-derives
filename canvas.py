import sympy as sp
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
import numpy as np
from sympy.abc import x

from fonction_couple import FonctionCouple


class Canvas(FigureCanvasQTAgg):
    __fig: plt.Figure
    __model: FonctionCouple

    def __init__(self, model: FonctionCouple):
        # création d'une figure matplotlib
        self.__fig, self.__ax = plt.subplots(1, 2)

        # appel du constructeur parent avec la fig en parametre
        super().__init__(self.__fig)

        # garder la référence sur le modèle
        self.__model = model
        self.dessiner()

    def dessiner(self):
        self.__ax[0].clear()
        self.__ax[1].clear()  # Efface les anciens axes

        # Génération des points x pour l'évaluation
        if self.__model.fonction is not None:
            try:
                x_vals = np.linspace(self.__model.x_min, self.__model.x_max, 500)

                # 1. Tracé de la fonction originale sur le premier axe
                f_numerique = sp.lambdify(self.__model.x, self.__model.fonction, "numpy")
                y_orig = f_numerique(x_vals)

                # Gestion du cas où f(x) est une constante
                if isinstance(y_orig, (int, float, np.number)):
                    y_orig = np.full_like(x_vals, y_orig)

                self.__ax[0].plot(x_vals, y_orig, color=self.__model.couleur)

                # 2. Calcul et tracé de la fonction dérivée sur le second axe
                expr_derivee = sp.diff(self.__model.fonction, self.__model.x)
                f_derivee_numerique = sp.lambdify(self.__model.x, expr_derivee, "numpy")
                y_deriv = f_derivee_numerique(x_vals)

                if isinstance(y_deriv, (int, float, np.number)):
                    y_deriv = np.full_like(x_vals, y_deriv)

                self.__ax[1].plot(x_vals, y_deriv, color=self.__model.couleur)

            except Exception as e:
                print(f"Erreur lors du tracé : {e}")

        # Appliquer explicitement les bornes de l'axe x sur les graphiques
        self.__ax[0].set_xlim(self.__model.x_min, self.__model.x_max)
        self.__ax[1].set_xlim(self.__model.x_min, self.__model.x_max)

        # Configuration des titres
        self.__ax[0].set_title("Fonction originale")
        self.__ax[1].set_title("Fonction dérivée")

        # Affichage de la grille
        self.__ax[0].grid(True)
        self.__ax[1].grid(True)

        # Rafraîchissement du canvas Qt
        self.draw()