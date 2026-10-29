from typing import override

from sympy import Expr

from fonction import Fonction

class FonctionPrincipale(Fonction):

    # Conctructeur de FonctionPrincipale avec la fonction
    def __init__(self, fonction : Expr, couleur : str):
        super().__init__(fonction, couleur)

    # repr de FonctionPrincipale : retourne les valeurs de la fonction
    # en précisant qu'il s'agit de la fonction principale
    @override
    def __repr__(self):
        return f"Fonction principale | {super().__repr__()}"