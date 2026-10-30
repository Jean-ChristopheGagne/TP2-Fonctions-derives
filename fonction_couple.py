from PyQt6.QtCore import QObject, pyqtSignal
from sympy import Expr

from fonction_derivee import FonctionDerivee
from fonction_principale import FonctionPrincipale
import sympy as sp

class FonctionCouple(QObject):

    # La fonction principale du couple
    # Attribut principale
    __fonction_principale : FonctionPrincipale

    # La fonction dérivée de la fonction principale
    # Attribut dérivée
    __fonction_derivee : FonctionDerivee

    # La variable x : cet attribut est le même pour tout les objets de FonctionCouple
    # Symbole x
    __x : Expr = sp.symbols("x")

    # La valeur de x minimale pour laquelle la fonction est définie sur le canvas
    # X min
    __x_min: float

    # La valeur maximale de x pour laquelle la fonction est définie sur le canvas
    # X max
    __x_max: float

    # Définition du signal personnalisé
    # Signal changé
    changed = pyqtSignal()

    # Constructeur de la classe Fonction couple avec posibilité d'aucun argument
    # Init
    def __init__(self, f_str: str = "", couleur_f_princ: str = "blue", couleur_f_der: str = "red"):
        # Super init
        super().__init__()
        # Min par défaut
        self.__x_min = 0.0
        # Max par défaut
        self.__x_max = 10.0

        # Si aucun texte n'est fourni, on initialise à None sans crasher
        # Définit l'expression
        fonc_princ_expr = FonctionCouple.definir_fonction_principale(f_str)

        # C'est ici qu'on associe chaque couleur à son objet respectif :
        # Crée principale
        self.__fonction_principale = FonctionPrincipale(fonc_princ_expr, couleur_f_princ)
        # Crée dérivée
        self.__fonction_derivee = FonctionDerivee(fonc_princ_expr, couleur_f_der)

    # Accesseur de la fonction principale
    # Propriété principale
    @property
    def fonction_principale(self):
        # Retourne principale
        return self.__fonction_principale

    # Muttateur de la fonction principale
    # Setter principale
    @fonction_principale.setter
    def fonction_principale(self, value: FonctionPrincipale):
        # Assigne valeur
        self.__fonction_principale = value
        # Si valide
        if value is not None and value.fonction is not None:
            # Change origine dérivée
            self.__fonction_derivee.changer_fonc_orig(value.fonction)
        # Sinon
        else:
            # Met None
            self.__fonction_derivee.changer_fonc_orig(None)
        # Émet changé
        self.changed.emit()

    # Accesseur de la fonction dérivée
    # Propriété dérivée
    @property
    def fonction_derivee(self):
        # Retourne dérivée
        return self.__fonction_derivee

    # Accesseur de la variable x de la classe
    # Classe x
    @classmethod
    def x(cls):
        # Retourne x
        return cls.__x

    # Accesseur de la valeur de x minimale
    # Propriété x_min
    @property
    def x_min(self):
        # Retourne x_min
        return self.__x_min

    # Muttateur de la valeur de x minimale
    # Setter x_min
    @x_min.setter
    def x_min(self, value: float):
        # Valide
        if self.valider_x_min(value):
            # Assigne x_min
            self.__x_min = value
            # Émet changé
            self.changed.emit()
        # Sinon
        else:
            # Erreur
            raise ValueError("Valeur interdite")

    # Accesseur de la valeur de x maximale
    # Propriété x_max
    @property
    def x_max(self):
        # Retourne x_max
        return self.__x_max

    # Muttateur de la valeur de x maximale
    # Setter x_max
    @x_max.setter
    def x_max(self, value: float):
        # Valide
        if self.valider_x_max(value):
            # Assigne x_max
            self.__x_max = value
            # Émet changé
            self.changed.emit()
        # Sinon
        else:
            # Erreur
            raise ValueError("Valeur interdite")

    # Validateur de la fonction principale entré en paramètre du constructeur
    # Valide fonction
    @classmethod
    def valider_fonction(cls, f_str: str) -> bool:
        # Si vide
        if f_str is None or str(f_str).strip() == "":
            # Autorise vide
            return True

        # critères de valdité de l'expression
        # Bool expression
        expression_possible : bool
        # Bool algébrique
        expresion_algebrique : bool
        # Bool variables
        variables_valides : bool

        # autres variables
        # Symbole x local
        x = sp.symbols('x')
        # Expr
        expr : Expr

        # vérification de la possibilité d'une expression
        # Essaye sympify
        try:
            # Parse
            expr = Expr(sp.sympify(f_str))
            # Vrai
            expression_possible = True
        # Erreur
        except (sp.SympifyError, TypeError):
            # Faux
            return False

        # vérification que l'expression est une expression algébrique
        # Vérifie algébrique
        expression_algebrique = expr.is_algebraic_expr()

        # vérification de les variables sont valides
        # Si constante
        if expr.is_constant():
            # Valide
            variables_valides = True
        # Sinon
        else:
            # Vérifie x
            variables_valides = expr.free_symbols == {x}

        # somme de tous les critères
        # Retourne bool global
        return expression_possible and expression_algebrique and variables_valides

    # Définit fonction
    @classmethod
    def definir_fonction_principale(cls, f_str: str) -> Expr:
        """
        Cette méthode définit la fonction principale entré en paramètre du constructeur
        :param f_str: la chaine de la fonction entré en paramètre
        :return: la fonction principale en forme d'expresion
        """
        # Si vide
        if f_str is None or str(f_str).strip() == "":
            # Retourne 0
            return sp.Integer(0)
        # Si valide
        if cls.valider_fonction(f_str):
            # Retourne expr
            return Expr(sp.sympify(f_str))
        # Sinon
        else:
            # Erreur
            raise ValueError("Expression invalide")

    # Validateur du x_min
    # Valide min
    def valider_x_min(self, x_min : float) -> bool:
        # Retourne bool
        return x_min < self.x_max

    # Validateur du x_max
    # Valide max
    def valider_x_max(self, x_max : float) -> bool:
        # Retourne bool
        return x_max > self.x_min