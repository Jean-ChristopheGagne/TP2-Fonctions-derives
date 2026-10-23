from sympy import Expr

from fonction_derivee import FonctionDerivee
from fonction_principale import FonctionPrincipale
import sympy as sp

class FonctionCouple:

    __fonction_principale : FonctionPrincipale
    __fonction_derivee : FonctionDerivee
    __x: Expr

    def __init__(self, f_str : str, couleur_f_princ : str, couleur_f_der : str, x_min : float, x_max : float):
        self.__x = sp.symbols("x")
        self.__fonction_principale = FonctionPrincipale(FonctionCouple.definir_fonction_principale(f_str), couleur_f_princ, x_min, x_max)

    @property
    def fonction_derivee(self):
        return self.__fonction_derivee

    @classmethod
    def valider_fonction(cls, f_str : str) -> bool:
        x = sp.symbols('x')
        expr = None
        expression_possible : bool
        expression_algebrique : bool
        variables_valides : bool
        try:
            expr = sp.sympify(f_str)
            expression_possible = True
        except (sp.SympifyError, TypeError):
            expression_possible = False
        expression_algebrique = expr.is_algebraic_expr()
        if expr.is_constant():
            variables_valides = True
        else :
            variables_valides = expr.free_symbols == {x}
        return expression_possible and expression_algebrique and variables_valides

    @classmethod
    def definir_fonction_principale(cls, f_str : str) -> Expr:
        if cls.valider_fonction(f_str):
            return Expr(sp.sympify(f_str))
        else:
            raise ValueError("Expression invalide")