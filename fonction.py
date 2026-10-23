import sympy as sp
from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QColorDialog
from sympy import Expr

class Fonction(QObject):

    __expr_fonction: Expr
    __Xmin: Expr
    __Xmax: Expr
    __couleur: QColorDialog
    __x: Expr

    def __init__(self):
        super().__init__()
        self.__x = sp.symbols("x")
        self.__expr_fonction = None
        self.__couleur = couleur

    @property
    def fonction(self):
        return self.__expr_fonction

    @fonction.setter
    def fonction(self, value: str):
        if self.valider_fonction(value):
            fonction = sp.sympify(value)
            self.__expr_fonction = sp.lambdify(self.variable, fonction, 'numpy')

    # @property
    # def function_derivee(self):
    #     return self.__fonctionDerivee
    #
    # @function_derivee.setter
    # def function_derivee(self, value: str):
    #     if self.valider_fonction(value):
    #         fonction = sp.sympify(value)
    #         self.__fonctionDerivee = sp.lambdify(self.variable, fonction, 'numpy')

    # @property
    # def titre(self):
    #     return self.__titre
    #
    # @titre.setter
    # def titre(self, value):
    #     self.__titre = value

    # @property
    # def showGrille(self):
    #     return self.__showGrille

    # @showGrille.setter
    # def showGrille(self, value):
    #     self.__showGrille = value

    @property
    def couleur(self):
        return self.__couleur

    @couleur.setter
    def couleur(self, setter_couleur):
        self.__couleur = setter_couleur

    @property
    def variable(self):
        return self.__x

    def valider_fonction(self, f_str) -> bool:
        try:
            expr = sp.sympify(f_str)
            symbols = expr.free_symbols
            return symbols.issubset({self.variable})
        except (sp.SympifyError, TypeError):
            return False
    def setter_couleur(self):
        couleur = QColorDialog.getColor()
        if couleur.isValid():
            print(couleur.name())  # Affiche la couleur en format hexadécimal