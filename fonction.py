from abc import ABC, ABCMeta
import sympy as sp
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.sip import wrappertype
from sympy import Expr
import matplotlib.colors as mcolors

# Définition de la métaclasse pour résoudre le conflit PyQt6 (wrappertype) et ABC (ABCMeta)
# Métaclasse
class MetaClasseFonction(wrappertype, ABCMeta):
    # Pass
    pass

# Classe Fonction
class Fonction(QObject, ABC, metaclass=MetaClasseFonction):

    # Définition du signal personnalisé
    # Signal changé
    changed = pyqtSignal()
    # Fonction décrite par l'objet
    # Attribut fonction
    _fonction : Expr
    # Couleur de la fonction
    # Attribut couleur
    _couleur : str
    # Variable indépendante de toutes les fonctions : la valeur ne doit pas être modifiée
    # Symbole x
    __x : Expr = sp.symbols("x")

    # Constructeur de Fonction avec la fonction et sa couleur
    # Init
    def __init__(self, fonction : Expr, couleur : str):
        # appel du constructeur parent de QObject  # Super init
        super().__init__()

        # Remplissage des attributs
        # Assigne fonction
        self._fonction = fonction
        # Assigne couleur
        self.couleur = couleur

    # Accesseur de la fonction
    # Propriété fonction
    @property
    def fonction(self):
        # Retourne fonction
        return self._fonction

    # Muttateur de la fonction
    # Setter fonction
    @fonction.setter
    def fonction(self, value : Expr):
        # Modifie fonction
        self._fonction = value
        # Émet un signal  # Émet changé
        self.changed.emit()

    # Accesseur de la couleur
    # Propriété couleur
    @property
    def couleur(self):
        # Retourne couleur
        return self._couleur

    # Muttateur de la couleur
    # Setter couleur
    @couleur.setter
    def couleur(self, value : str):
        # Valide couleur
        if Fonction.valider_couleur(value) :
            # Modifie couleur
            self._couleur = value
            # Émet un signal  # Émet changé
            self.changed.emit()
        # Sinon
        else :
            # Erreur
            raise ValueError("Couleur impossible")

    # Accesseur de la variable
    # Classe x
    @classmethod
    def x(cls):
        # Retourne x
        return cls.__x

    # Validateur de la couleur
    # Statique valider
    @staticmethod
    def valider_couleur(couleur : str):
        # Retourne bool
        return mcolors.is_color_like(couleur)