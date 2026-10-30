from typing import override

from sympy import Expr
import sympy as sp

from fonction import Fonction

class FonctionDerivee(Fonction):

    # La fonction d'origine
    # Attribut origine
    __fonc_orig : Expr

    # Contructeur de la fonction dérivée à partir de la fonction d'origine
    # Init
    def __init__(self, fonc_orig : Expr, couleur : str):
        # On vérifie si fonc_orig n'est pas None avant d'appliquer sp.diff
        # Calcule dérivée
        derivee = sp.diff(fonc_orig, self.x()) if fonc_orig is not None else None
        # Super init
        super().__init__(derivee, couleur)
        # Sauve origine
        self.__fonc_orig = fonc_orig

    # Méthode classe
    @classmethod
    def determiner_derivee(cls, fonction_originale : Expr) -> Expr:
        """
        Cette méthode détermine la dérivé de la fonction d'origine
        :param fonction_originale: la fonction d'origine
        :return: la fonction dérivée de la fonction d'origine
        """
        # Diff SymPy
        return sp.diff(fonction_originale, Fonction.x())

    # Tangente point
    def tan_un_point(self, valeur_x : float) -> float:
        """
        Cette méthode donne le taux de variation de la tangente en un point x de la fonction.
        :param valeur_x: la valeur de x pour la tangente recherchée
        :return: le taux de variation de la tangente de l'équation au x recherché
        """
        # Substitue x
        return self.fonction.subs(Fonction.x(), valeur_x)

    # Ordonnée origine
    def ord_orig_tan_un_point(self, valeur_x : float) -> float:
        """
        Cette méthode donne l'ordonné à l'orgine de l'équation tangente en un point x de la fonction
        :param valeur_x: la valeur de x pour le la tangente recherchée
        :return: l'ordonnée à l'origine de l'équation tangente de la fonction au point x recherché
        """
        # Pente
        taux_var : float = self.tan_un_point(valeur_x)
        # Valeur y
        valeur_y : float = float(self.__fonc_orig.subs(Fonction.x(), valeur_x).evalf())
        # Calcul b
        return valeur_y - valeur_x * taux_var

    # Équation tangente
    def eq_tan_un_point(self, valeur_x : float) -> Expr:
        """
        Cette méthode retourne l'équation de la fonction tangente en un point x de la fonction
        :param valeur_x: la valeur de x pour l'équation tangente recherchée
        :return: l'équation de la fonction tangente de la fonction au point x recherché
        """
        # Retourne équation
        return self.tan_un_point(valeur_x) * Fonction.x() + self.ord_orig_tan_un_point(valeur_x)

    # repr de FonctionDerivee : retourne les valeurs de la fonction
    # en précisant que c'est une fonction dérivée
    # Repr
    @override
    def __repr__(self):
        # Retourne format
        return f"Fonction dérivée | Fonction d'origine : {self.__fonc_orig} | {super().__repr__()}"

    # Change origine
    def changer_fonc_orig(self, nouv_fonc : Expr):
        """
        Cette méthode change la fonction d'origine si elle est changer dans le graphique
        :param nouv_fonc: la nouvelle fonction d'origine
        """
        # Ré-init
        self.__init__(nouv_fonc, self.couleur)