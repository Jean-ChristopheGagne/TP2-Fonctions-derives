from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QPushButton, QLineEdit, QMainWindow, QCheckBox, QColorDialog, QVBoxLayout
from PyQt6.uic import loadUi

from canvas import Canvas
from fonction import Fonction


class FenetrePrincipale:

    __model : Fonction
    matplotlibVLayout : QVBoxLayout
    fonctionLineEdit : QLineEdit
    titreLineEdit : QLineEdit
    afficherGrilleCheckBox : QCheckBox
    dessinerPushButtton : QPushButton
    actionCouleur : QAction

    def __init__(self):
        super().__init__()
        loadUi("ui/exercice2.ui", self)

        # instance du model
        self.__model = Fonction()

        # création du canvas et ajout au layout
        self.matplotlibVLayout.addWidget(Canvas(self.__model))

        # connection du lineEdit de la fonction
        self.fonctionLineEdit.editingFinished.connect(lambda : self.__model.fonction(self.fonctionLineEdit.text))

    @property
    def model(self):
        return self.__model