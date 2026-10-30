from typing import override

from PyQt6.QtCore import QObject, pyqtSignal
from sympy import Expr

from fonction_derivee import FonctionDerivee
from fonction_principale import FonctionPrincipale
import sympy as sp

class FonctionCouple(QObject):

    # La fonction principale du couple
    __fonction_principale : FonctionPrincipale

    # La fonction dérivée de la fonction principale
    __fonction_derivee : FonctionDerivee

    # La variable x : cet attribut est le même pour tout les objets de FonctionCouple
    __x : Expr = sp.symbols("x")

    # La valeur de x minimale pour laquelle la fonction est définie sur le canvas
    __x_min: float

    # La valeur maximale de x pour laquelle la fonction est définie sur le canvas
    __x_max: float

    # Définition du signal personnalisé
    changed = pyqtSignal()

    # Constructeur de la classe Fonction couple avec posibilité d'aucun argument
    def __init__(self, f_str: str = "", couleur_f_princ: str = "blue", couleur_f_der: str = "red"):
        super().__init__()
        self.__x_min = 0.0
        self.__x_max = 10.0

        # Si aucun texte n'est fourni, on initialise à None sans crasher
        fonc_princ_expr = FonctionCouple.definir_fonction_principale(f_str)

        # C'est ici qu'on associe chaque couleur à son objet respectif :
        self.__fonction_principale = FonctionPrincipale(fonc_princ_expr, couleur_f_princ)
        self.__fonction_derivee = FonctionDerivee(fonc_princ_expr, couleur_f_der)

    # Accesseur de la fonction principale
    @property
    def fonction_principale(self):
        return self.__fonction_principale

    # Muttateur de la fonction principale
    @fonction_principale.setter
    def fonction_principale(self, value: FonctionPrincipale):
        self.__fonction_principale = value
        if value is not None and value.fonction is not None:
            self.__fonction_derivee.changer_fonc_orig(value.fonction)
        else:
            self.__fonction_derivee.changer_fonc_orig(None)
        self.changed.emit()

    # Accesseur de la fonction dérivée
    @property
    def fonction_derivee(self):
        return self.__fonction_derivee

    # Accesseur de la variable x de la classe
    @classmethod
    def x(cls):
        return cls.__x

    # Accesseur de la valeur de x minimale
    @property
    def x_min(self):
        return self.__x_min

    # Muttateur de la valeur de x minimale
    @x_min.setter
    def x_min(self, value: float):
        if self.valider_x_min(value):
            self.__x_min = value
            self.changed.emit()
        else:
            raise ValueError("Valeur interdite")

    # Accesseur de la valeur de x maximale
    @property
    def x_max(self):
        return self.__x_max

    # Muttateur de la valeur de x maximale
    @x_max.setter
    def x_max(self, value: float):
        if self.valider_x_max(value):
            self.__x_max = value
            self.changed.emit()
        else:
            raise ValueError("Valeur interdite")

    # Validateur de la fonction principale entré en paramètre du constructeur
    @classmethod
    def valider_fonction(cls, f_str: str) -> bool:
        if f_str is None or str(f_str).strip() == "":
            return True  # On autorise les valeurs vides au démarrage

        # critères de valdité de l'expression
        expression_possible : bool
        expresion_algebrique : bool
        variables_valides : bool

        # autres variables
        x = sp.symbols('x')
        expr : Expr

        # vérification de la possibilité d'une expression
        try:
            expr = Expr(sp.sympify(f_str))
            expression_possible = True
        except (sp.SympifyError, TypeError):
            return False

        # vérification que l'expression est une expression algébrique
        expression_algebrique = expr.is_algebraic_expr()

        # vérification de les variables sont valides
        if expr.is_constant():
            variables_valides = True
        else:
            variables_valides = expr.free_symbols == {x}

        # somme de tous les critères
        return expression_possible and expression_algebrique and variables_valides

    @classmethod
    def definir_fonction_principale(cls, f_str: str) -> Expr:
        """
        Cette méthode définit la fonction principale entré en paramètre du constructeur
        :param f_str: la chaine de la fonction entré en paramètre
        :return: la fonction principale en forme d'expresion
        """
        if f_str is None or str(f_str).strip() == "":
            return sp.Integer(0)
        if cls.valider_fonction(f_str):
            return Expr(sp.sympify(f_str))
        else:
            raise ValueError("Expression invalide")

    # Validateur du x_min
    def valider_x_min(self, x_min : float) -> bool:
        return x_min < self.x_max

    # Validateur du x_max
    def valider_x_max(self, x_max : float) -> bool:
        return x_max > self.x_min

    # repr de la classe FonctionCouple
    @override
    def __repr__(self):
        return f"Fonction de base : {self.fonction_principale.fonction} | Couleur fonction de base {self.fonction_principale.couleur} | Fonction dérivée {self.fonction_derivee.fonction} | Couleur fonction dérivée : {self.fonction_derivee.couleur} | x min : {self.x_min} | x max : {self.x_max}"