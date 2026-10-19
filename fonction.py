class Fonction :

    __fonction: Expr
    __couleur: None
    __titre: str
    __showGrille: bool
    __x: Expr

    def __init__(self):
        super().__init__()
        self.__x = sp.symbols("x")
        self.__fonction = None
        self.__showGrille = False
        self.__titre = None
        self.__couleur = None

    @property
    def fonction(self):
        return self.__fonction

    @fonction.setter
    def fonction(self, value: str):
        if self.valider_fonction(value):
            fonction = sp.sympify(value)
            self.__fonction = sp.lambdify(self.variable, fonction, 'numpy')

    @property
    def titre(self):
        return self.__titre

    @titre.setter
    def titre(self, value):
        self.__titre = value

    @property
    def showGrille(self):
        return self.__showGrille

    @showGrille.setter
    def showGrille(self, value):
        self.__showGrille = value

    @property
    def couleur(self):
        return self.__couleur

    @couleur.setter
    def couleur(self, value):
        self.__couleur = value

    @property
    def variable(self):
        return self.__x

    def valider_fonction(self, f_str) -> bool:
        pass