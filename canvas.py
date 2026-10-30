import sympy as sp
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
import numpy as np

from fonction_couple import FonctionCouple

class Canvas(FigureCanvasQTAgg):
    # Type figure
    __fig: plt.Figure
    # Type modèle
    __model: FonctionCouple

    # Constructeur
    def __init__(self, model: FonctionCouple):
        # création d'une figure matplotlib
        # Crée deux axes
        self.__fig, self.__ax = plt.subplots(1, 2)

        # appel du constructeur parent avec la fig en parametre
        # Init parent
        super().__init__(self.__fig)

        # garder la référence sur le modèle
        # Stocke le modèle
        self.__model = model
        # Dessine
        self.dessiner()

    # Méthode dessin
    def dessiner(self):
        # Efface axe 0
        self.__ax[0].clear()
        # Efface les anciens axes  # Efface axe 1
        self.__ax[1].clear()

        # Vérification si la fonction principale et son expression existent
        # Vérifie la fonction
        if self.__model.fonction_principale is not None and self.__model.fonction_principale.fonction is not None:
            # Bloc try
            try:
                # Crée un tableau de 500 points de même distance entre x_min et x_max pour tracer les graphiques
                # Crée les x
                x_vals = np.linspace(self.__model.x_min, self.__model.x_max, 500)

                # Récupération de l'expression SymPy de la fonction principale
                # Récupère l'expression
                expr_princ = self.__model.fonction_principale.fonction

                # Tracé de la fonction originale sur le premier axe
                # Lambdify SymPy
                f_numerique = sp.lambdify(FonctionCouple.x(), expr_princ, "numpy")
                # Calcule y
                y_orig = f_numerique(x_vals)

                # Gestion du cas où f(x) est une constante
                # Si scalaire
                if isinstance(y_orig, (int, float, np.number)):
                    # Remplit le tableau
                    y_orig = np.full_like(x_vals, y_orig)

                # Pour la fonction originale (axe 0) :
                # Récupère couleur
                couleur_princ = self.__model.fonction_principale.couleur
                # Trace l'originale
                self.__ax[0].plot(x_vals, y_orig, color=couleur_princ)

                # Calcul et tracé de la fonction dérivée sur le second axe
                # Si dérivée existe
                if self.__model.fonction_derivee.fonction is not None:
                    # Récupère dérivée
                    expr_derivee = self.__model.fonction_derivee.fonction
                    # Récupère couleur
                    couleur_deriv = self.__model.fonction_derivee.couleur

                    # Lambdify dérivée
                    f_derivee_numerique = sp.lambdify(FonctionCouple.x(), expr_derivee, "numpy")
                    # Calcule y dérivée
                    y_deriv = f_derivee_numerique(x_vals)

                    # Si constante
                    if isinstance(y_deriv, (int, float, np.number)):
                        # Remplit tableau
                        y_deriv = np.full_like(x_vals, y_deriv)

                    # Trace dérivée
                    self.__ax[1].plot(x_vals, y_deriv, color=couleur_deriv)

            # Saisit l'erreur
            except Exception as e:
                # Affiche l'erreur
                print(f"Erreur lors du tracé : {e}")

        # Appliquer explicitement les bornes de l'axe x sur les graphiques
        # Limite x axe 0
        self.__ax[0].set_xlim(self.__model.x_min, self.__model.x_max)
        # Limite x axe 1
        self.__ax[1].set_xlim(self.__model.x_min, self.__model.x_max)

        # Configuration des titres
        # Titre axe 0
        self.__ax[0].set_title("Fonction originale")
        # Titre axe 1
        self.__ax[1].set_title("Fonction dérivée")

        # Affichage de la grille
        # Grille axe 0
        self.__ax[0].grid(True)
        # Grille axe 1
        self.__ax[1].grid(True)

        # Rafraîchissement du canvas Qt
        # Redessine
        self.draw()