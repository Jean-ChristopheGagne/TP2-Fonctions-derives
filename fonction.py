from abc import ABC

import sympy as sp
from PyQt6.QtCore import QObject
from sympy import Expr
import matplotlib.colors as mcolors

class Fonction(ABC,QObject):

    _fonction : Expr
    _couleur : str
    _x : Expr

    def __init__(self, fonction : Expr, couleur : str):
        super().__init__()
        self._x = sp.symbols("x")
        self._fonction = fonction
        self.couleur = couleur

    @property
    def fonction(self):
        return self._fonction

    @fonction.setter
    def fonction(self, value : Expr):
        self._fonction = value

    @property
    def couleur(self):
        return self._couleur

    @couleur.setter
    def couleur(self, value : str):
        if Fonction.valider_couleur(value) :
            self._couleur = value
        else :
            raise ValueError("Couleur impossible")

    @property
    def x(self):
        return self._x

    @staticmethod
    def valider_couleur(couleur : str):
        return mcolors.is_color_like(couleur)

    def __repr__(self):
        return f"Expression : {self.fonction} | Couleur : {self.couleur}"