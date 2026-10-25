from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QLineEdit, QMainWindow, QVBoxLayout, QDoubleSpinBox, QLabel, QColorDialog
from PyQt6.uic import loadUi

from canvas import Canvas
from fonction import Fonction


class FenetrePrincipale(QMainWindow):

    __model : Fonction
    matplotlibVLayout : QVBoxLayout
    fonctionEdit : QLineEdit
    actionCouleur : QAction
    labelTangeance: QLabel
    labelDerivee: QLabel
    labelVariation: QLabel
    SpinXmin : QDoubleSpinBox
    SpinXmax : QDoubleSpinBox
    _couleur: QColorDialog


    def __init__(self):
        super().__init__()
        loadUi("ui/tp2derivee.ui", self)

        # instance du model
        self.__model = Fonction(None, "blue", 0.0, 10.0)

        # création et stockage du canvas dans un attribut self.__canvas
        self.__canvas = Canvas(self.__model)
        self.matplotlibVLayout.addWidget(self.__canvas)

        # connection du lineEdit de la fonction
        self.fonctionEdit.editingFinished.connect(lambda : self.__model.fonction(self.fonctionEdit.text))

        # Connexion de l'action du menu au changement de couleur
        self.actionCouleur.triggered.connect(self.changement_couleur)

        # Connexions des SpinBox pour Xmin et Xmax
        self.SpinXmin.valueChanged.connect(self.changement_Xmin)
        self.SpinXmax.valueChanged.connect(self.changement_Xmax)

    @property
    def model(self):
        return self.__model

    def changement_couleur(self):
        couleur = QColorDialog.getColor()
        if couleur.isValid():
            self.__model.couleur = couleur.name()  # Met à jour la couleur dans le modèle
            self.__canvas.dessiner()  # Redessine le graphique avec la nouvelle couleur

    def changement_Xmin(self, valeur: float):
        """Met à jour Xmin dans le modèle et redessine le graphique."""
        self.__model.x_min = valeur
        self.__canvas.dessiner()

    def changement_Xmax(self, valeur: float):
        """Met à jour Xmax dans le modèle et redessine le graphique."""
        self.__model.x_max = valeur
        self.__canvas.dessiner()