import json
import warnings

import sympy as sp
from PyQt6.QtCore import QAbstractListModel, Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QDoubleSpinBox, QLabel, QColorDialog, QSlider, \
    QComboBox, QFileDialog, QPushButton
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
    actionEditeurFonction: QAction
    labelTangeance: QLabel
    labelDerivee: QLabel
    labelVariation: QLabel
    SpinXmin : QDoubleSpinBox
    SpinXmax : QDoubleSpinBox
    __couleur: QColorDialog
    slider: QSlider
    __fonctionListView: QAbstractListModel
    ajouterFichiers: QPushButton


    def __init__(self):
        super().__init__()
        loadUi("ui/tp2derivee.ui", self)

        warnings.filterwarnings('ignore', category=RuntimeWarning)

        # Définir une taille initiale plus grande (largeur, hauteur en pixels)
        self.resize(1200, 800)

        # Instance du modèle global (FonctionCouple)
        self.__model = FonctionCouple()

        # Création et stockage du canvas
        self.__canvas = Canvas(self.__model)
        self.matplotlibVLayout.addWidget(self.__canvas)

        # Connexion du signal du modèle pour redessiner automatiquement
        self.__model.changed.connect(self.__canvas.dessiner)

        # Mettre à jour les labels sous les graphiques
        self.__model.changed.connect(self.actualiser_labels_par_defaut)

        # Connexion de l'action du menu au changement de couleur
        self.actionCouleurOriginale.triggered.connect(self.changement_couleur_originale)
        self.actionCouleurDerivee.triggered.connect(self.changement_couleur_derivee)

        # Connexions des SpinBox pour Xmin et Xmax
        self.SpinXmin.setValue(0.0)
        self.SpinXmax.setValue(10.0)
        # Permettre aux SpinBox d'accepter des nombres négatifs
        self.SpinXmin.setMinimum(-500.0)
        self.SpinXmin.setMaximum(500.0)
        self.SpinXmax.setMinimum(-500.0)
        self.SpinXmax.setMaximum(500.0)
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
        #Instanciation en premier de la fenêtre dockable d'édition de fonctions

        # S'assurer qu'il est bien visible à l'instanciation et connecter l'action du menu
        self.editeurFonction.setVisible(True)
        self.actionEditeurFonction.triggered.connect(self.basculer_affichage_editeur)

        # Récupération du modèle et liaison avec le ComboBox
        self.__fonctionListView = self.editeurFonction.modele
        self.fonctionEdit.setModel(self.__fonctionListView)
        self.fonctionEdit.currentTextChanged.connect(self.changement_fonction)

        # Connexion du bouton Fichiers situé dans l'éditeur dockable
        if hasattr(self.editeurFonction, 'ajouterFichiers'):
            self.editeurFonction.ajouterFichiers.clicked.connect(self.ouvrir_fichier_json)

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

    def basculer_affichage_editeur(self):
        """Bascule l'affichage du dock widget (le cache s'il est visible, l'affiche s'il est caché)."""
        if self.editeurFonction.isVisible():
            self.editeurFonction.hide()
        else:
            self.editeurFonction.show()

    def changement_Xmin(self, valeur: float):
        self.SpinXmax.setMinimum(valeur + 0.1)
        self.__model.x_min = valeur

    def changement_Xmax(self, valeur: float):
        self.SpinXmin.setMaximum(valeur - 0.1)
        self.__model.x_max = valeur

    def changement_fonction(self, texte: str):
        """Récupère le texte de l'input, le convertit en SymPy et redessine."""
        try:
            couleur_actuelle = self.__model.fonction_principale.couleur
            if not texte or texte.strip() == "":
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
            print(f"Erreur dans l'expression de la fonction ('{texte}') : {e}")

    def mettre_a_jour_variation(self, valeur_x: float):
        """Calcule et affiche le taux de variation, le point de tangence et la dérivée en évitant les erreurs de domaine."""
        try:
            # Gestion du point de tangence (x, y) de la fonction principale
            if self.__model.fonction_principale.fonction is not None:
                expr_orig = self.__model.fonction_principale.fonction

                # Évaluation sécurisée pour éviter les erreurs de domaine (ex: log(0) ou sqrt négatif)
                try:
                    y_val_complex = expr_orig.subs(self.__model.x, valeur_x).evalf()
                    # Si le résultat est complexe (ex: racine d'un nombre négatif), on gère ou on ignore
                    if y_val_complex.is_real:
                        y_val = float(y_val_complex)
                        texte_tangeance = f"({valeur_x:.2f} ; {y_val:.2f})"
                        self.labelTangeance.setText(texte_tangeance)
                    else:
                        self.labelTangeance.setText("Indéfini (complexe)")
                except Exception:
                    self.labelTangeance.setText("Indéfini")
            else:
                self.labelTangeance.setText("")

            # Vérifie si la fonction dérivée existe dans le modèle
            if self.__model.fonction_derivee.fonction is not None:
                derivee_obj = self.__model.fonction_derivee
                try:
                    taux_complex = derivee_obj.tan_un_point(valeur_x)
                    if hasattr(taux_complex, 'is_real') and taux_complex.is_real:
                        taux = float(taux_complex)
                        self.labelVariation.setText(f"x = {valeur_x:.2f}) : {taux:.5f}")
                    else:
                        # Si c'est déjà un float ou évaluable
                        taux = float(taux_complex)
                        self.labelVariation.setText(f"x = {valeur_x:.2f}) : {taux:.5f}")
                except Exception:
                    self.labelVariation.setText(f"x = {valeur_x:.2f}) : Indéfini")
            else:
                self.labelVariation.setText(f"x = {valeur_x}")

            # Affichage labelDerivee
            if self.__model.fonction_derivee.fonction is not None:
                expr_deriv = self.__model.fonction_derivee.fonction
                self.labelDerivee.setText(f"{expr_deriv}")
            else:
                self.labelDerivee.setText("")

        except Exception as e:
            print(f"Erreur lors de la mise à jour des labels : {e}")
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

    def actualiser_labels_par_defaut(self):
        """Met à jour les labels automatiquement dès que le modèle change."""
        # Tu peux prendre la valeur actuelle du slider ou une valeur par défaut (ex: 0.0)
        if hasattr(self, 'slider'):
            valeur_x = self.slider.value() / self.__facteur_precision
        else:
            valeur_x = 0.0

        self.mettre_a_jour_variation(valeur_x)

    def ouvrir_fichier_json(self):
        """Ouvre l'explorateur de fichiers pour sélectionner un JSON et l'ajoute au modèle."""
        chemin_fichier, _ = QFileDialog.getOpenFileName(
            self, "Ouvrir un fichier de fonctions JSON", "", "Fichiers JSON (*.json);;Tous les fichiers (*)"
        )

        if chemin_fichier:
            try:
                with open(chemin_fichier, 'r', encoding='utf-8') as f:
                    donnees = json.load(f)

                for item in donnees:
                    expr_str = item.get("expression")
                    couleur = item.get("couleur", "blue")

                    if expr_str:
                        expr = sp.sympify(expr_str)
                        nouvelle_fonction = FonctionPrincipale(expr, couleur)

                        # Ajout au modèle partagé (met à jour instantanément la ListView et le ComboBox)
                        self.editeurFonction.modele.add_item(nouvelle_fonction)

                print("Fichier JSON chargé avec succès !")
            except Exception as e:
                print(f"Erreur lors du chargement du fichier JSON : {e}")