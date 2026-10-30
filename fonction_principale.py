from typing import override

from sympy import Expr

from fonction import Fonction

class FonctionPrincipale(Fonction):
    # Conctructeur de FonctionPrincipale avec la fonction
    # Init
    def __init__(self, fonction : Expr, couleur : str):
        # Super init
        super().__init__(fonction, couleur)

    # repr de FonctionPrincipale : retourne les valeurs de la fonction
    # en précisant qu'il s'agit de la fonction principale
    # Repr
    @override
    def __repr__(self):
        # Retourne format
        return f"Fonction principale | {super().__repr__()}"