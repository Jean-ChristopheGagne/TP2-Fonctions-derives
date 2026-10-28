import sympy as sp
from PyQt6.QtCore import QAbstractListModel, Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QDoubleSpinBox, QLabel, QColorDialog, QSlider, \
    QComboBox
from PyQt6.uic import loadUi

from canvas import Canvas
from fenetre_list_fonction import FenetreListFonction
from fonction_couple import FonctionCouple
from fonction_principale import FonctionPrincipale


class FenetrePrincipale(QMainWindow):

    __model : FonctionCouple
    matplotlibVLayout : QVBoxLayout
    fonctionEdit : QComboBox
    actionCouleurOriginale : QAction
    actionCouleurDerivee : QAction
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

        # Instance du modèle global (FonctionCouple)
        self.__model = FonctionCouple()

        # Création et stockage du canvas
        self.__canvas = Canvas(self.__model)
        self.matplotlibVLayout.addWidget(self.__canvas)

        # Connexion du signal du modèle pour redessiner automatiquement
        self.__model.changed.connect(self.__canvas.dessiner)

        # Connexion de l'action du menu au changement de couleur
        self.actionCouleurOriginale.triggered.connect(self.changement_couleur_originale)
        self.actionCouleurDerivee.triggered.connect(self.changement_couleur_derivee)

        # Connexions des SpinBox pour Xmin et Xmax
        self.SpinXmin.setValue(0.0)
        self.SpinXmax.setValue(10.0)
        self.SpinXmin.valueChanged.connect(self.changement_Xmin)
        self.SpinXmax.valueChanged.connect(self.changement_Xmax)

        # Facteur pour le nombre de décimales constantes pour la valeur de x (100 = deux décimales)
        self.__facteur_precision = 100

        # Connection du slider avec sa méthode
        self.slider.valueChanged.connect(self.sur_changement_slider)

        # Initialisation des limites du slider en fonction des SpinBox
        self.ajuster_limites_slider()

        # Connexion des SpinBox pour réajuster le slider si l'utilisateur change les bornes
        self.SpinXmin.valueChanged.connect(self.ajuster_limites_slider)
        self.SpinXmax.valueChanged.connect(self.ajuster_limites_slider)

        # Initialisation de la fenêtre dockable d'édition de fonctions
        self.editeurFonction = FenetreListFonction(parent=self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.editeurFonction)   # affiche le dock widget à droite

        # Récupération du modèle et liaison avec le ComboBox
        self.__fonctionListView = self.editeurFonction.modele
        self.fonctionEdit.setModel(self.__fonctionListView)
        self.fonctionEdit.currentTextChanged.connect(self.changement_fonction)

    @property
    def model(self):
        return self.__model

    def changement_couleur_originale(self):
        couleur = QColorDialog.getColor()
        if couleur.isValid():
            # Modifie uniquement la couleur de la fonction principale
            self.__model.fonction_principale.couleur = couleur.name()
            self.__canvas.dessiner()

    def changement_couleur_derivee(self):
        couleur = QColorDialog.getColor()
        if couleur.isValid():
            # Modifie uniquement la couleur de la fonction dérivée
            self.__model.fonction_derivee.couleur = couleur.name()
            self.__canvas.dessiner()

    def changement_Xmin(self, valeur: float):
        self.SpinXmax.setMinimum(valeur + 0.1)
        self.__model.x_min = valeur

    def changement_Xmax(self, valeur: float):
        self.SpinXmin.setMaximum(valeur - 0.1)
        self.__model.x_max = valeur

    def changement_fonction(self):
        """Récupère le texte de l'input, le convertit en SymPy et redessine."""
        texte = self.fonctionEdit.currentText()
        try:
            couleur_actuelle = self.__model.fonction_principale.couleur
            if texte.strip() == "":
                # On assigne une FonctionPrincipale vide
                self.__model.fonction_principale = FonctionPrincipale(None, couleur_actuelle)
            else:
                expr = sp.sympify(texte)
                # On met à jour via une instance de FonctionPrincipale
                self.__model.fonction_principale = FonctionPrincipale(expr, couleur_actuelle)

            self.fonctionEdit.setStyleSheet("")
            self.__canvas.dessiner()
        except Exception as e:
            self.fonctionEdit.setStyleSheet("background-color: #ffcccc;")
            print(f"Erreur dans l'expression de la fonction : {e}")

    def mettre_a_jour_variation(self, valeur_x: float):
        """Calcule et affiche la valeur de la dérivée (taux de variation) pour un x donné."""
        try:
            # Vérifie si la fonction dérivée existe dans le modèle
            if self.__model.fonction_derivee.fonction is not None:
                # Utilise la méthode de ta classe FonctionDerivee pour évaluer en un point
                derivee_obj = self.__model.fonction_derivee
                # On évalue la dérivée et on s'assure d'avoir un float
                taux = float(derivee_obj.tan_un_point(valeur_x))

                # Formatage strict à 5 décimales pour le taux de variation
                texte_affiche = f"Taux de variation (en x = {valeur_x:.2f}) : {taux:.5f}"
                self.labelVariation.setText(texte_affiche)
            else:
                self.labelVariation.setText(f"x = {valeur_x}")
        except Exception as e:
            print(f"Erreur lors du calcul du taux de variation : {e}")

    def ajuster_limites_slider(self):
        """Ajuste les bornes du slider en multipliant par le facteur de 5 décimales."""
        min_val = self.SpinXmin.value()
        max_val = self.SpinXmax.value()

        self.slider.setMinimum(int(min_val * self.__facteur_precision))
        self.slider.setMaximum(int(max_val * self.__facteur_precision))

    def sur_changement_slider(self, valeur_entiere: int):
        """Convertit la valeur entière du slider en un float arrondi à 5 décimales exactes."""
        valeur_x = valeur_entiere / self.__facteur_precision

        # Formatage pour s'assurer d'avoir toujours l'affichage avec 5 décimales fixes
        valeur_x_formatee = round(valeur_x, 5)

        # Exemple d'utilisation avec ton taux de variation :
        self.mettre_a_jour_variation(valeur_x_formatee)