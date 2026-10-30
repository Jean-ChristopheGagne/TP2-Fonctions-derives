import json
import sympy as sp
from PyQt6.QtCore import QAbstractListModel, Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QDoubleSpinBox, QLabel, QColorDialog, QSlider, \
    QComboBox, QFileDialog
from PyQt6.uic import loadUi

from canvas import Canvas
from fenetre_list_fonction import FenetreListFonction
from fonction_couple import FonctionCouple
from fonction_principale import FonctionPrincipale


class FenetrePrincipale(QMainWindow):

    # Modèle
    __model : FonctionCouple
    # Layout canvas
    matplotlibVLayout : QVBoxLayout
    # ComboBox fonctions
    fonctionEdit : QComboBox
    # Action couleur originale
    actionCouleurOriginale : QAction
    # Action couleur dérivée
    actionCouleurDerivee : QAction
    # Action éditeur
    actionEditeurFonction: QAction
    # Label tangence
    labelTangeance: QLabel
    # Label dérivée
    labelDerivee: QLabel
    # Label variation
    labelVariation: QLabel
    # Spinbox X min
    SpinXmin : QDoubleSpinBox
    # Spinbox X max
    SpinXmax : QDoubleSpinBox
    # Dialogue couleur
    __couleur: QColorDialog
    # Slider x
    slider: QSlider
    # Modèle liste
    __fonctionListView: QAbstractListModel


    # Init
    def __init__(self):
        # Super init
        super().__init__()
        # Charge ui
        loadUi("ui/tp2derivee.ui", self)

        # Définir une taille initiale plus grande (largeur, hauteur en pixels)
        # Redimensionne
        self.resize(1200, 800)

        # Instance du modèle global (FonctionCouple)
        # Crée modèle
        self.__model = FonctionCouple()

        # Création et stockage du canvas
        # Crée canvas
        self.__canvas = Canvas(self.__model)
        # Ajoute au layout
        self.matplotlibVLayout.addWidget(self.__canvas)

        # Connexion du signal du modèle pour redessiner automatiquement
        # Connecte signal dessin
        self.__model.changed.connect(self.__canvas.dessiner)

        # Mettre à jour les labels sous les graphiques
        # Connecte labels
        self.__model.changed.connect(self.actualiser_labels_par_defaut)

        # Connexion de l'action du menu au changement de couleur
        # Connecte couleur originale
        self.actionCouleurOriginale.triggered.connect(self.changement_couleur_originale)
        # Connecte couleur dérivée
        self.actionCouleurDerivee.triggered.connect(self.changement_couleur_derivee)

        # Connexions des SpinBox pour Xmin et Xmax
        # Valeur min
        self.SpinXmin.setValue(0.0)
        # Valeur max
        self.SpinXmax.setValue(10.0)
        # Permettre aux SpinBox d'accepter des nombres négatifs
        # Min min
        self.SpinXmin.setMinimum(-500.0)
        # Min max
        self.SpinXmin.setMaximum(500.0)
        # Max min
        self.SpinXmax.setMinimum(-500.0)
        # Max max
        self.SpinXmax.setMaximum(500.0)
        # Connecte min
        self.SpinXmin.valueChanged.connect(self.changement_Xmin)
        # Connecte max
        self.SpinXmax.valueChanged.connect(self.changement_Xmax)

        # Facteur pour le nombre de décimales constantes pour la valeur de x (100 = deux décimales)
        # Facteur précision
        self.__facteur_precision = 100

        # Connection du slider avec sa méthode
        # Connecte slider
        self.slider.valueChanged.connect(self.sur_changement_slider)

        # Initialisation des limites du slider en fonction des SpinBox
        # Ajuste slider
        self.ajuster_limites_slider()

        # Connexion des SpinBox pour réajuster le slider si l'utilisateur change les bornes
        # Connecte spin min
        self.SpinXmin.valueChanged.connect(self.ajuster_limites_slider)
        # Connecte spin max
        self.SpinXmax.valueChanged.connect(self.ajuster_limites_slider)

        # Initialisation de la fenêtre dockable d'édition de fonctions
        # Crée dock
        self.editeurFonction = FenetreListFonction(parent=self)
        # affiche le dock widget à droite
        # Ajoute dock
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.editeurFonction)
        #Instanciation en premier de la fenêtre dockable d'édition de fonctions

        # S'assurer qu'il est bien visible à l'instanciation et connecter l'action du menu
        # Rend visible
        self.editeurFonction.setVisible(True)
        # Connecte action menu
        self.actionEditeurFonction.triggered.connect(self.basculer_affichage_editeur)

        # Récupération du modèle et liaison avec le ComboBox
        # Récupère modèle
        self.__fonctionListView = self.editeurFonction.modele
        # Assigne ComboBox
        self.fonctionEdit.setModel(self.__fonctionListView)
        # Connecte texte
        self.fonctionEdit.currentTextChanged.connect(self.changement_fonction)

        # Connexion du signal personnalisé de l'éditeur vers la méthode d'ouverture de fichier
        self.editeurFonction.fichiers_clique.connect(self.ouvrir_fichier_json)

    # Propriété modèle
    @property
    def model(self):
        # Retourne modèle
        return self.__model

    # Change couleur originale
    def changement_couleur_originale(self):
        # Dialogue couleur
        couleur = QColorDialog.getColor()
        # Si valide
        if couleur.isValid():
            # Modifie uniquement la couleur de la fonction principale
            # Assigne couleur
            self.__model.fonction_principale.couleur = couleur.name()
            # Redessine
            self.__canvas.dessiner()

    # Change couleur dérivée
    def changement_couleur_derivee(self):
        # Dialogue couleur
        couleur = QColorDialog.getColor()
        # Si valide
        if couleur.isValid():
            # Modifie uniquement la couleur de la fonction dérivée
            # Assigne couleur
            self.__model.fonction_derivee.couleur = couleur.name()
            # Redessine
            self.__canvas.dessiner()

    # Bascule éditeur
    def basculer_affichage_editeur(self):
        """Bascule l'affichage du dock widget (le cache s'il est visible, l'affiche s'il est caché)."""
        # Si visible
        if self.editeurFonction.isVisible():
            # Cache
            self.editeurFonction.hide()
        # Sinon
        else:
            # Montre
            self.editeurFonction.show()

    # Change X min
    def changement_Xmin(self, valeur: float):
        # Ajuste max
        self.SpinXmax.setMinimum(valeur + 0.1)
        # Assigne modèle
        self.__model.x_min = valeur

    # Change X max
    def changement_Xmax(self, valeur: float):
        # Ajuste min
        self.SpinXmin.setMaximum(valeur - 0.1)
        # Assigne modèle
        self.__model.x_max = valeur

    # Change fonction
    def changement_fonction(self, texte: str):
        """Récupère le texte de l'input, le convertit en SymPy et redessine."""
        # Try convert
        try:
            # Sauve couleur
            couleur_actuelle = self.__model.fonction_principale.couleur
            # Si vide
            if not texte or texte.strip() == "":
                # On assigne une FonctionPrincipale vide
                # Crée vide
                self.__model.fonction_principale = FonctionPrincipale(None, couleur_actuelle)
            # Sinon
            else:
                # Sympify
                expr = sp.sympify(texte)
                # On met à jour via une instance de FonctionPrincipale
                # Crée principale
                self.__model.fonction_principale = FonctionPrincipale(expr, couleur_actuelle)

            # Style normal
            self.fonctionEdit.setStyleSheet("")
            # Redessine
            self.__canvas.dessiner()
        # Saisit erreur
        except Exception as e:
            # Style rouge
            self.fonctionEdit.setStyleSheet("background-color: #ffcccc;")
            # Print erreur
            print(f"Erreur dans l'expression de la fonction ('{texte}') : {e}")

    # Met à jour variation
    def mettre_a_jour_variation(self, valeur_x: float):
        """Calcule et affiche le taux de variation, le point de tangeance pour un x donné et la dérivée dans les labels appropriés."""
        # Try eval
        try:
            # Vérifie si la fonction dérivée existe dans le modèle
            # Si dérivée existe
            if self.__model.fonction_derivee.fonction is not None:
                # Utilise la méthode de la classe FonctionDerivee pour évaluer en un point
                # Récupère dérivée
                derivee_obj = self.__model.fonction_derivee
                # On évalue la dérivée et on s'assure d'avoir un float
                # Calcule taux
                taux = float(derivee_obj.tan_un_point(valeur_x))

                # Affichage dans labelVariation
                # Formate texte
                texte_affiche = f"x = {valeur_x:.2f}) : {taux:.5f}"
                # Affiche label
                self.labelVariation.setText(texte_affiche)
            # Sinon
            else:
                # Affiche x simple
                self.labelVariation.setText(f"x = {valeur_x}")

            # Gestion du point de tangence (x, y) de la fonction principale
            # Si principale existe
            if self.__model.fonction_principale.fonction is not None:
                # On évalue la fonction d'origine pour trouver y à partir de x
                # Récupère expression
                expr_orig = self.__model.fonction_principale.fonction
                # Calcule y
                y_val = float(expr_orig.subs(self.__model.x(), valeur_x))

                # Affichage dans labelTangeance
                # Formate point
                texte_tangeance = f"({valeur_x:.2f} ; {y_val:.2f})"
                # Affiche label
                self.labelTangeance.setText(texte_tangeance)
            # Sinon
            else:
                # Vide label
                self.labelTangeance.setText("")
                #Affichage labelDerivee
            # Si dérivée existe
            if self.__model.fonction_derivee.fonction is not None:
                # Récupère dérivée
                expr_deriv = self.__model.fonction_derivee.fonction
                # Affiche label
                self.labelDerivee.setText(f"{expr_deriv}")
            # Sinon
            else:
                # Vide label
                self.labelDerivee.setText("")

        # Saisit erreur
        except Exception as e:
            # Print erreur
            print(f"Erreur lors de la mise à jour des labels : {e}")

    # Ajuste limites slider
    def ajuster_limites_slider(self):
        """Ajuste les bornes du slider en multipliant par le facteur de 5 décimales."""
        # Récupère min
        min_val = self.SpinXmin.value()
        # Récupère max
        max_val = self.SpinXmax.value()

        # Set min slider
        self.slider.setMinimum(int(min_val * self.__facteur_precision))
        # Set max slider
        self.slider.setMaximum(int(max_val * self.__facteur_precision))

    # Sur changement slider
    def sur_changement_slider(self, valeur_entiere: int):
        """Convertit la valeur entière du slider en un float arrondi à 5 décimales exactes."""
        # Calcule x
        valeur_x = valeur_entiere / self.__facteur_precision

        # Formatage pour s'assurer d'avoir toujours l'affichage avec 5 décimales fixes
        # Arrondit
        valeur_x_formatee = round(valeur_x, 5)

        # Exemple d'utilisation avec ton taux de variation :
        # Met à jour variation
        self.mettre_a_jour_variation(valeur_x_formatee)

    # Actualise labels défaut
    def actualiser_labels_par_defaut(self):
        """Met à jour les labels automatiquement dès que le modèle change."""
        # Tu peux prendre la valeur actuelle du slider ou une valeur par défaut (ex: 0.0)
        # Si slider existe
        if hasattr(self, 'slider'):
            # Calcule x
            valeur_x = self.slider.value() / self.__facteur_precision
        # Sinon
        else:
            # Défaut 0
            valeur_x = 0.0

        # Met à jour variation
        self.mettre_a_jour_variation(valeur_x)

        # Ouvre l'explorateur de fichiers pour charger un fichier JSON de fonctions   (utilisation de l'IA)
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
                            self.editeurFonction.modele.add_item(nouvelle_fonction)

                    print("Fichier JSON chargé avec succès !")
                except Exception as e:
                    print(f"Erreur lors du chargement du fichier JSON : {e}")