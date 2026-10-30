import sympy as sp
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
import numpy as np

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

        # Vérification si la fonction principale et son expression existent
        if self.__model.fonction_principale is not None and self.__model.fonction_principale.fonction is not None:
            try:
                # Crée un tableau de 500 points de même distance entre x_min et x_max pour tracer les graphiques
                x_vals = np.linspace(self.__model.x_min, self.__model.x_max, 500)

                # Récupération de l'expression SymPy de la fonction principale
                expr_princ = self.__model.fonction_principale.fonction
                couleur_princ = self.__model.fonction_principale.couleur

                # Tracé de la fonction originale sur le premier axe
                f_numerique = sp.lambdify(FonctionCouple.x(), expr_princ, "numpy")
                y_orig = f_numerique(x_vals)

                # Gestion du cas où f(x) est une constante
                if isinstance(y_orig, (int, float, np.number)):
                    y_orig = np.full_like(x_vals, y_orig)

                # Pour la fonction originale (axe 0) :
                couleur_princ = self.__model.fonction_principale.couleur
                self.__ax[0].plot(x_vals, y_orig, color=couleur_princ)

                # Calcul et tracé de la fonction dérivée sur le second axe
                if self.__model.fonction_derivee.fonction is not None:
                    expr_derivee = self.__model.fonction_derivee.fonction
                    couleur_deriv = self.__model.fonction_derivee.couleur

                    f_derivee_numerique = sp.lambdify(FonctionCouple.x(), expr_derivee, "numpy")
                    y_deriv = f_derivee_numerique(x_vals)

                    if isinstance(y_deriv, (int, float, np.number)):
                        y_deriv = np.full_like(x_vals, y_deriv)

                    self.__ax[1].plot(x_vals, y_deriv, color=couleur_deriv)

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