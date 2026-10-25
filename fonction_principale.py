from sympy import Expr

from fonction import Fonction

class FonctionPrincipale(Fonction):

    def __init__(self, fonction : Expr, couleur : str, x_min : float, x_max : float):
        super().__init__(fonction, couleur, x_min, x_max)