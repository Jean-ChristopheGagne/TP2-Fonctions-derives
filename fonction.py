from abc import ABC
import sympy as sp
from PyQt6.QtCore import QObject
from sympy import Expr
import matplotlib.colors as mcolors

class Fonction(ABC, QObject):

    _fonction : Expr
    _x_min : float
    _x_max : float
    _couleur : str
    _x : Expr

    def __init__(self, fonction : Expr, couleur : str, x_min : float, x_max : float):
        super().__init__()
        self._x = sp.symbols("x")
        self._fonction = fonction
        self._x_min = x_min
        self._x_max = x_max
        self.couleur = couleur

    @property
    def fonction(self):
        return self._fonction

    @fonction.setter
    def fonction(self, value : Expr):
        self._fonction = value

    @property
    def couleur(self):
        return self.__couleur

    @couleur.setter
    def couleur(self, value : str):
        if Fonction.valider_couleur(value) :
            self.__couleur = value
        else :
            raise ValueError("Couleur impossible")

    @property
    def x(self):
        return self._x

    @property
    def x_min(self):
        return self._x_min

    @x_min.setter
    def x_min(self, value : float):
        self._x_min = value

    @property
    def x_max(self):
        return self._x_max

    @x_max.setter
    def x_max(self, value : float):
        self._x_max = value

    @staticmethod
    def valider_couleur(couleur : str) -> bool:
        return mcolors.is_color_like(couleur)