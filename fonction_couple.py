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

    def __init__(self, f_str: str = None, couleur_f_princ: str = "blue", couleur_f_der: str = "red"):
        super().__init__()
        self.__x = sp.symbols("x")
        self.__x_min = 0.0
        self.__x_max = 10.0

        # Si aucun texte n'est fourni, on initialise à None sans crasher
        fonc_princ_expr = FonctionCouple.definir_fonction_principale(f_str) if f_str else None

        # C'est ici qu'on associe chaque couleur à son objet respectif :
        self.__fonction_principale = FonctionPrincipale(fonc_princ_expr, couleur_f_princ)
        self.__fonction_derivee = FonctionDerivee(fonc_princ_expr, couleur_f_der)

    @property
    def fonction_principale(self):
        return self.__fonction_principale

    @fonction_principale.setter
    def fonction_principale(self, value: FonctionPrincipale):
        self.__fonction_principale = value
        if value is not None and value.fonction is not None:
            self.__fonction_derivee.changer_fonc_orig(value.fonction)
        else:
            self.__fonction_derivee.changer_fonc_orig(None)
        self.changed.emit()

    @property
    def fonction_derivee(self):
        return self.__fonction_derivee

    @property
    def x(self):
        return self.__x

    @property
    def x_min(self):
        return self.__x_min

    @x_min.setter
    def x_min(self, value: float):
        if self.valider_x_min(value):
            self.__x_min = value
            self.changed.emit()
        else:
            raise ValueError("Valeur interdite")

    @property
    def x_max(self):
        return self.__x_max

    @x_max.setter
    def x_max(self, value: float):
        if self.valider_x_max(value):
            self.__x_max = value
            self.changed.emit()
        else:
            raise ValueError("Valeur interdite")

    @classmethod
    def valider_fonction(cls, f_str: str) -> bool:
        if f_str is None or str(f_str).strip() == "":
            return True  # On autorise les valeurs vides au démarrage

        x = sp.symbols('x')
        try:
            expr = sp.sympify(f_str)
            expression_possible = True
        except (sp.SympifyError, TypeError):
            return False

        expression_algebrique = expr.is_algebraic_expr()
        if expr.is_constant():
            variables_valides = True
        else:
            variables_valides = expr.free_symbols == {x}
        return expression_possible and expression_algebrique and variables_valides

    @classmethod
    def definir_fonction_principale(cls, f_str: str) -> Expr:
        if f_str is None or str(f_str).strip() == "":
            return None
        if cls.valider_fonction(f_str):
            return sp.sympify(f_str)
        else:
            raise ValueError("Expression invalide")

    def valider_x_min(self, x_min : float) -> bool:
        return x_min < self.x_max

    def valider_x_max(self, x_max : float) -> bool:
        return x_max > self.x_min