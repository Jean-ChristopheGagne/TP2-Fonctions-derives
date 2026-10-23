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
    __Xmin: QDoubleSpinBox
    __Xmax: QDoubleSpinBox
    __couleur: QColorDialog


    def __init__(self):
        super().__init__()
        loadUi("ui/tp2derivee.ui", self)

        # instance du model
        self.__model = Fonction()

        # création du canvas et ajout au layout
        self.matplotlibVLayout.addWidget(Canvas(self.__model))

        # connection du lineEdit de la fonction
        self.fonctionEdit.editingFinished.connect(lambda : self.__model.fonction(self.fonctionEdit.text))

        triggered.connect(self.changement_couleur()))

        # # Création du menu Setting
        menu_file = self.menuBar("Setting")
        menu_file.addAction("Couleur")

    @property
    def model(self):
        return self.__model

    def changement_couleur(self):
     couleur = QColorDialog.getColor()
     if couleur.isValid():
        print(couleur.name())  # Affiche la couleur en format hexadécimal