from sympy import Expr
import sympy as sp

from fonction import Fonction

class FonctionDerivee(Fonction):

    def __init__(self,fonction_original : Expr, couleur : str, x_min : float, x_max : float):
        super().__init__()

    @classmethod
    def determiner_derivee(cls, Expr) -> Expr:
        return sp.d