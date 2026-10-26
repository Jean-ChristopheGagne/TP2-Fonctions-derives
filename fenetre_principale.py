import sympy as sp
from PyQt6.QtCore import QAbstractListModel
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QDoubleSpinBox, QLabel, QColorDialog, QSlider, \
    QComboBox
from PyQt6.uic import loadUi

from canvas import Canvas
from fenetre_list_fonction import FenetreListFonction
from fonction import Fonction


class FenetrePrincipale(QMainWindow):

    __model : Fonction
    matplotlibVLayout : QVBoxLayout
    fonctionEdit : QComboBox
    actionCouleur : QAction
    labelTangeance: QLabel
    labelDerivee: QLabel
    labelVariation: QLabel
    SpinXmin : QDoubleSpinBox
    SpinXmax : QDoubleSpinBox
    __couleur: QColorDialog
    slider: QSlider
    __fonctionListView: QAbstractListModel


    def __init__(self):
        super().__init__()
        loadUi("ui/tp2derivee.ui", self)

        # instance du model
        self.__model = Fonction(None, "blue")

        # création et stockage du canvas dans un attribut self.__canvas
        self.__canvas = Canvas(self.__model)
        self.matplotlibVLayout.addWidget(self.__canvas)

        # Connexion de l'action du menu au changement de couleur
        self.actionCouleur.triggered.connect(self.changement_couleur)

        # Connexions des SpinBox pour Xmin et Xmax
        self.SpinXmin.valueChanged.connect(self.changement_Xmin)
        self.SpinXmax.valueChanged.connect(self.changement_Xmax)
########################################################Continuer################################################
        self.editeurFonction = FenetreListFonction(parent=self)

        self.fonctionEdit.setModel(self.__fonctionListView)    # affiche ComboBox

    ###############################################################################################################

    @property
    def model(self):
        return self.__model

    def changement_couleur(self):
        couleur = QColorDialog.getColor()
        if couleur.isValid():
            self.__model.couleur = couleur.name()  # Met à jour la couleur dans le modèle
            self.__canvas.dessiner()  # Redessine les graphiques avec la nouvelle couleur

    def changement_Xmin(self, valeur: float):
        """Met à jour Xmin et force le maximum de SpinXmax à rester supérieur."""
        # Empêche le SpinXmax de descendre en dessous ou égal à la nouvelle valeur de Xmin
        self.SpinXmax.setMinimum(valeur + 0.1)

        self.__model.x_min = valeur
        self.__canvas.dessiner()

    def changement_Xmax(self, valeur: float):
        """Met à jour Xmax et force le minimum de SpinXmin à rester inférieur."""
        # Empêche le SpinXmin de monter au-dessus ou égal à la nouvelle valeur de Xmax
        self.SpinXmin.setMaximum(valeur - 0.1)

        self.__model.x_max = valeur
        self.__canvas.dessiner()

    def changement_fonction(self):
        """Récupère le texte de l'input, le convertit en SymPy et redessine."""
        texte = self.fonctionEdit.text()
        try:
            if texte.strip() == "":
                self.__model.fonction = None
            else:
                # Convertit la chaîne de caractères en expression mathématique SymPy
                self.__model.fonction = sp.sympify(texte)

            # Si la conversion réussit : on réinitialise le style (fond normal)
            self.fonctionEdit.setStyleSheet("")

            # Redessine le canvas avec la nouvelle fonction
            self.__canvas.dessiner()
        except Exception as e:
            # Si une erreur survient (expression invalide) : on met le fond en rouge clair
            self.fonctionEdit.setStyleSheet("background-color: #ffcccc;")
            print(f"Erreur dans l'expression de la fonction : {e}")