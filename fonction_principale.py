from sympy import Expr

from fonction import Fonction

class FonctionPrincipale(Fonction):

    def __init__(self, fonction : Expr, couleur : str):
        super().__init__(fonction, couleur)

    def __repr__(self):
        return f"Fonction principale | {super().__repr__()}"