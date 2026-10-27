from PyQt6.QtCore import QObject, pyqtSignal
from sympy import Expr

from fonction_derivee import FonctionDerivee
from fonction_principale import FonctionPrincipale
import sympy as sp

class FonctionCouple(QObject):

    __fonction_principale : FonctionPrincipale
    __fonction_derivee : FonctionDerivee
    __x: Expr
    __x_min: float
    __x_max: float

    # Définition du signal personnalisé
    changed = pyqtSignal()

    def __init__(self, f_str : str, couleur_f_princ : str, couleur_f_der : str):
        super().__init__()
        self.__x = sp.symbols("x")
        self.__fonction_principale = FonctionPrincipale(FonctionCouple.definir_fonction_principale(f_str), couleur_f_princ)
        self.__fonction_derivee = FonctionDerivee(FonctionCouple.definir_fonction_principale(f_str), couleur_f_der)
        self.verifier_couleurs()

    @property
    def fonction_principale(self):
        return self.__fonction_principale

    @fonction_principale.setter
    def fonction_principale(self, value : FonctionPrincipale):
        self.__fonction_principale = value
        self.__fonction_derivee.changer_fonc_orig(value.fonction)

    @property
    def fonction_derivee(self):
        return self.__fonction_derivee

    @property
    def x_min(self):
        return self.__x_min

    @x_min.setter
    def x_min(self, value: float):
        if self.valider_x_min(value):
            self.__x_min = value
            self.changed.emit()  # Émet un signal
        else:
            raise ValueError("Valeur interdite")

    @property
    def x_max(self):
        return self.__x_max

    @x_max.setter
    def x_max(self, value: float):
        if self.valider_x_max(value):
            self.__x_max = value
            self.changed.emit()  # Émet un signal
        else:
            raise ValueError("Valeur interdite")

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

    def valider_x_min(self, x_min : float) -> bool:
        return -10.0 < x_min < self.x_max

    def valider_x_max(self, x_max : float) -> bool:
        return -10.0 < x_max < self.x_min

    def verifier_couleurs(self):
        if self.fonction_principale.couleur == self.fonction_derivee.couleur:
            raise ValueError("Couleurs équivalente")