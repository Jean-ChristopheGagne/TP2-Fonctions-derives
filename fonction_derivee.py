from sympy import Expr
import sympy as sp

from fonction import Fonction

class FonctionDerivee(Fonction):

    __fonc_orig : Expr

    def __init__(self, fonc_orig : Expr, couleur : str):
        super().__init__(self.determiner_derivee(fonc_orig), couleur)
        self.__fonc_orig = fonc_orig

    def determiner_derivee(self, fonction_originale : Expr) -> Expr:
        return sp.diff(fonction_originale, self.x)

    def tan_un_point(self, valeur_x : float) -> float:
        return self.fonction.subs(self.x, valeur_x)

    def ord_orig_tan_un_point(self, valeur_x : float) -> float:
        taux_var : float = self.tan_un_point(valeur_x)
        valeur_y : float = self.__fonc_orig.subs(self.x, valeur_x)
        return valeur_y - valeur_x * taux_var

    def eq_tan_un_point(self, valeur_x : float) -> Expr:
        return self.tan_un_point(valeur_x) * self.x + self.ord_orig_tan_un_point(valeur_x)

    def __repr__(self):
        return f"Fonction dérivée | Fonction d'origine : {self.__fonc_orig} | {super().__repr__()}"

    def changer_fonc_orig(self, nouv_fonc : Expr):
        self.__init__(nouv_fonc, self.couleur)