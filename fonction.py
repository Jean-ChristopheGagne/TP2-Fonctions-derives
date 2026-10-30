from abc import ABC, ABCMeta
import sympy as sp
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.sip import wrappertype
from sympy import Expr
import matplotlib.colors as mcolors

# Définition de la métaclasse pour résoudre le conflit PyQt6 (wrappertype) et ABC (ABCMeta)
class MetaClasseFonction(wrappertype, ABCMeta):
    pass

class Fonction(QObject, ABC, metaclass=MetaClasseFonction):

    # Définition du signal personnalisé
    changed = pyqtSignal()
    # Fonction décrite par l'objet
    _fonction : Expr
    # Couleur de la fonction
    _couleur : str
    # Variable indépendante de toutes les fonctions : la valeur ne doit pas être modifiée
    __x : Expr = sp.symbols("x")

    # Constructeur de Fonction avec la fonction et sa couleur
    def __init__(self, fonction : Expr, couleur : str):
        super().__init__() # appel du constructeur parent de QObject

        # Remplissage des attributs
        self._fonction = fonction
        self.couleur = couleur

    # Accesseur de la fonction
    @property
    def fonction(self):
        return self._fonction

    # Muttateur de la fonction
    @fonction.setter
    def fonction(self, value : Expr):
        self._fonction = value
        self.changed.emit()   # Émet un signal

    # Accesseur de la couleur
    @property
    def couleur(self):
        return self._couleur

    # Muttateur de la couleur
    @couleur.setter
    def couleur(self, value : str):
        if Fonction.valider_couleur(value) :
            self._couleur = value
            self.changed.emit()  # Émet un signal
        else :
            raise ValueError("Couleur impossible")

    # Accesseur de la variable
    @classmethod
    def x(cls):
        return cls.__x

    # Validateur de la couleur
    @staticmethod
    def valider_couleur(couleur : str):
        return mcolors.is_color_like(couleur)