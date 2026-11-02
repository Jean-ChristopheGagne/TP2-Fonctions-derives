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

    # Attribut privé pour stocker l'état d'affichage de la grille
    __grille_visible: bool

    # Définition du signal personnalisé
    changed = pyqtSignal()

    # Constructeur de la classe Fonction couple avec posibilité d'aucun argument
    def __init__(self, f_str: str = "", couleur_f_princ: str = "blue", couleur_f_der: str = "red"):
        super().__init__()
        self.__x_min = 0.0
        self.__x_max = 10.0

        # Initialise l'état de la grille à True par défaut au démarrage
        self.__grille_visible = True

        # Si aucun texte n'est fourni, on initialise à None sans crasher
        fonc_princ_expr = FonctionCouple.definir_fonction_principale(f_str)

        # C'est ici qu'on associe chaque couleur à son objet respectif :
        self.__fonction_principale = FonctionPrincipale(fonc_princ_expr, couleur_f_princ)
        self.__fonction_derivee = FonctionDerivee(fonc_princ_expr, couleur_f_der)

        # validation des couleurs
        self.valider_couleurs_fonction()
        self.fonction_principale.changed.connect(self.valider_couleurs_fonction)
        self.fonction_derivee.changed.connect(self.valider_couleurs_fonction)

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
            self.__fonction_derivee.changer_fonc_orig(sp.Integer(0))
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

    # Accesseur pour récupérer l'état de la grille
    @property
    def grille_visible(self) -> bool:
        # Retourne la valeur booléenne de la visibilité de la grille
        return self.__grille_visible

    # Mutteur pour modifier l'état de la grille
    @grille_visible.setter
    def grille_visible(self, visible: bool):
        # Met à jour l'attribut privé avec la nouvelle valeur
        self.__grille_visible = visible
        # Émet le signal pour prévenir le canvas qu'il doit se redessiner
        self.changed.emit()

    # Validateur de la fonction principale entré en paramètre du constructeur
    @classmethod
    def valider_fonction(cls, f_str: str) -> bool:
        if f_str is None or str(f_str).strip() == "":
             return True  # On autorise les valeurs vides au démarrage

        # critères de validité de l'expression
        expression_possible: bool
        variables_valides: bool

        # autres variables
        x = sp.symbols('x')
        expr: Expr

        # vérification de la possibilité d'une expression (avec contexte pour sin, cos, exp, sqrt, etc.)
        try:
            contexte_autorise = {
                'cos': sp.cos, 'sin': sp.sin, 'tan': sp.tan,
                'sqrt': sp.sqrt, 'log': sp.log, 'exp': sp.exp,
                'x': x
            }
            expr = sp.sympify(f_str, locals=contexte_autorise)
            expression_possible = True
        except (sp.SympifyError, TypeError):
            return False

        # vérification que les variables sont valides
        if expr.is_constant():
            variables_valides = True
        else:
            variables_valides = expr.free_symbols == {x}

        # Retourne le tout (on a retiré la restriction algébrique stricte pour laisser passer sin, cos, exp...)
        return expression_possible and variables_valides

    @classmethod
    def definir_fonction_principale(cls, f_str: str) -> Expr:
        """
        Cette méthode définit la fonction principale entrée en paramètre du constructeur
        :param f_str: la chaine de la fonction entrée en paramètre
        :return: la fonction principale en forme d'expression SymPy
        """
        if f_str is None or str(f_str).strip() == "":
            return sp.Integer(0)

        contexte_autorise = {
            'cos': sp.cos, 'sin': sp.sin, 'tan': sp.tan,
            'sqrt': sp.sqrt, 'log': sp.log, 'exp': sp.exp,
            'x': sp.symbols('x')
        }

        if cls.valider_fonction(f_str):
            # On retourne directement l'expression SymPy sans l'envelopper dans Expr()
            return sp.sympify(f_str, locals=contexte_autorise)
        else:
            raise ValueError("Expression invalide")

    # Validateur du x_min
    def valider_x_min(self, x_min : float) -> bool:
        return x_min <= self.x_max

    # Validateur du x_max
    def valider_x_max(self, x_max : float) -> bool:
        return x_max >= self.x_min

    # repr de la classe FonctionCouple
    @override
    def __repr__(self):
        return f"Fonction de base : {self.fonction_principale.fonction} | Couleur fonction de base {self.fonction_principale.couleur} | Fonction dérivée {self.fonction_derivee.fonction} | Couleur fonction dérivée : {self.fonction_derivee.couleur} | x min : {self.x_min} | x max : {self.x_max}"

    def changer_fonction_principale(self, f_str):
        """
        Cette méthode permet de changer la fonction principale avec la nouvelle String de la fonction
        :param f_str: la str de fonction principale
        """
        couleur_princ = self.fonction_principale.couleur
        self.fonction_principale = FonctionPrincipale(FonctionCouple.definir_fonction_principale(f_str), couleur_princ)

    # Cette méthode valide que les couleurs de la fonction principale et de la fonction dérivée ne soient pas équivalentes
    def valider_couleurs_fonction(self):
        if self.fonction_principale.couleur == self.fonction_derivee.couleur:
            raise ValueError("Couleurs de la fonction principale et de la fonction dérivée équivalentes")