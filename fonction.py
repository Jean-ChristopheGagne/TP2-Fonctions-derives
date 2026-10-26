from abc import ABC

import sympy as sp
from PyQt6.QtCore import QObject
from sympy import Expr
import matplotlib.colors as mcolors

class Fonction(ABC,QObject):

    # Définition d'un signal personnalisé qui annonce du changement
    changed = pyqtSignal()

    _fonction : Expr
    _couleur : str
    _x_min: float
    _x_max: float
    _x : Expr

    def __init__(self, fonction : Expr, couleur : str):
        super().__init__()
        self._x = sp.symbols("x")
        self._fonction = fonction
        self.couleur = couleur
        self._x_min = x_min
        self._x_max = x_max

    @property
    def fonction(self):
        return self._fonction

    @fonction.setter
    def fonction(self, value : Expr):
        self._fonction = value
        self.changed.emit()   #On émet le signal ici

    @property
    def couleur(self):
        return self._couleur

    @couleur.setter
    def couleur(self, value : str):
        if Fonction.valider_couleur(value) :
            self._couleur = value
            self.changed.emit()  #On émet le signal ici
        else :
            raise ValueError("Couleur impossible")

    @property
    def x_min(self):
        return self._x_min

    @x_min.setter
    def x_min(self, value: float):
        self._x_min = value
        self.changed.emit()  #On émet le signal ici

    @property
    def x_max(self):
        return self._x_max

    @x_max.setter
    def x_max(self, value: float):
        self._x_max = value
        self.changed.emit()  #On émet le signal ici


    @property
    def x(self):
        return self._x

    @staticmethod
    def valider_couleur(couleur : str):
        return mcolors.is_color_like(couleur)

    def __repr__(self):
        return f"Expression : {self.fonction} | Couleur : {self.couleur}"