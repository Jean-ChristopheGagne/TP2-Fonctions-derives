import json
import os

import sympy as sp
from PyQt6.QtCore import QAbstractListModel, Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QDoubleSpinBox, QLabel, QColorDialog, QSlider, \
    QComboBox, QFileDialog, QCheckBox, QMessageBox
from PyQt6.uic import loadUi

from canvas import Canvas
from fenetre_list_fonction import FenetreListFonction
from fonction_couple import FonctionCouple
from fonction_derivee import FonctionDerivee
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
    # CheckBox pour grille
    grilleBox: QCheckBox


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
        self.SpinXmin.setMinimum(-10.0)
        # Min max
        self.SpinXmin.setMaximum(10.0)
        # Max min
        self.SpinXmax.setMinimum(-10.0)
        # Max max
        self.SpinXmax.setMaximum(10.0)
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

        # S'assure que la case de la grille est cochée par défaut au démarrage
        self.grilleBox.setChecked(True)

        # Connecte le signal de changement d'état de la grilleBox à la méthode dédiée
        self.grilleBox.toggled.connect(self.changer_etat_grille)

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

        # Appelle la méthode pour charger les fonctions depuis le JSON dès le lancement
        self.charger_json_au_demarrage()

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
        # Modifie uniquement la couleur de la fonction principale
        # Assigne couleur
        try :
            self.__model.fonction_principale.couleur = couleur.name()
            # Redessine
            self.__canvas.dessiner()
        except ValueError as e :
            QMessageBox.warning(self, "Erreur de sélection de couleur", str(e))

    # Change couleur dérivée
    def changement_couleur_derivee(self):
        # Dialogue couleur
        couleur = QColorDialog.getColor()
        # Si valide
        # Modifie uniquement la couleur de la fonction principale
        # Assigne couleur
        try:
            self.__model.fonction_derivee.couleur = couleur.name()
            # Redessine
            self.__canvas.dessiner()
        except ValueError as e:
            QMessageBox.warning(self, "Erreur de sélection de couleur", str(e))

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
            self.__model.changer_fonction_principale(texte)
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
    def mettre_a_jour_variation(self, valeur_x: float):  # Aide de l'IA à certains points
        # Calcule et affiche le taux de variation, le point de tangence et la dérivée dans les labels appropriés
        derivee_obj : FonctionDerivee
        try:
            # Vérifie si la fonction dérivée existe dans le modèle
            if self.__model.fonction_derivee.fonction is not None:
                # Récupère l'objet dérivée
                derivee_obj = self.__model.fonction_derivee
                # Calcule la valeur brute de la pente en ce point
                valeur_brute = derivee_obj.tan_un_point(valeur_x)

                # Tente de convertir en float et d'afficher
                try:
                    # Convertit la valeur brute en décimal float
                    taux = float(valeur_brute)
                    # Affiche le résultat normal dans le label (2 et 5 chiffres après la virgule)
                    self.labelVariation.setText(f"x = {valeur_x:.2f} : {taux:.5f}")
                # Si la conversion plante (ex: nombre complexe ou infini)
                except:
                    # Affiche non défini proprement dans le label
                    self.labelVariation.setText(f"x = {valeur_x:.2f} : Non défini")
            # Sinon, si aucune dérivée n'existe
            else:
                # Affiche juste la valeur de x
                self.labelVariation.setText(f"x = {valeur_x}")

            # Gestion du point de tangence (x, y) de la fonction principale (maintenant au bon niveau d'indentation)
            if self.__model.fonction_principale.fonction is not None:
                # Récupère l'expression d'origine de la fonction
                expr_orig = self.__model.fonction_principale.fonction
                # Calcule y pour la valeur de x actuelle
                y_brut = expr_orig.subs(self.__model.x(), valeur_x)
                # Tente de convertir y en décimal float
                try:
                    # Convertit y en décimal
                    y_val = float(y_brut)
                    # Affiche les coordonnées (x, y) dans le label
                    self.labelTangeance.setText(f"({valeur_x:.2f} ; {y_val:.2f})")
                # Si la conversion de y échoue (ex: domaine invalide)
                except:
                    # Affiche non défini pour le point de tangence
                    self.labelTangeance.setText(f"({valeur_x:.2f} ; Non défini)")
            # Sinon, si pas de fonction principale
            else:
                # Vide le label de tangence
                self.labelTangeance.setText("")

            # Affichage de l'expression de la dérivée avec un formatage propre
            if self.__model.fonction_derivee.fonction is not None:
                # Récupère l'expression brute de la dérivée en texte
                expr_deriv_brute = str(derivee_obj.fonction)
                # Applique le formatage visuel pour rendre l'expression plus jolie
                expr_jolie = self.formater_expression_jolie(expr_deriv_brute)
                # Affiche l'expression formatée dans le label de la dérivée
                self.labelDerivee.setText(f"{expr_jolie}")
            # Sinon, si la dérivée est vide
            else:
                # Vide le label de la dérivée
                self.labelDerivee.setText("")

        # Saisit et intercepte toute autre erreur imprévue
        except Exception as e:
            # Affiche l'erreur dans la console pour le débogage
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

    # Méthode appelée lorsque l'utilisateur coche ou décoche la grilleBox
    def changer_etat_grille(self, etat: bool):
        # Transmet l'état de la case (True/False) au modèle global
        self.__model.grille_visible = etat

    def formater_expression_jolie(self, expr_str: str):          # Aide de l'IA
        if not expr_str:
            return ""

        # Remplacement des puissances (ex: x**2 -> x² )
        texte = expr_str.replace("**2", "²").replace("**3", "³")

        # Pour les puissances générales (ex: x**4 -> x⁴)
        remplacements_exposants = {
            "**0": "⁰", "**1": "¹", "**2": "²", "**3": "³", "**4": "⁴",
            "**5": "⁵", "**6": "⁶", "**7": "⁷", "**8": "⁸", "**9": "⁹"
        }
        #Fait l'action de remplacer "old" par "new"
        for k, v in remplacements_exposants.items():
            texte = texte.replace(k, v)

        # Nettoyage des multiplications superflues (ex: 3*x -> 3x)
        texte = texte.replace("*", "")

        return texte
#||||||||||||||||||||||||||||||||||||||||||||   Aide de l'IA   |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
    # Méthode commune pour importer et charger les fonctions depuis n'importe quel fichier JSON
    def importer_donnees_json(self, chemin_fichier: str):
        # Vérifie si le fichier spécifié existe physiquement sur le disque
        if os.path.exists(chemin_fichier):
            # Bloc try pour sécuriser la lecture et le traitement du fichier
            try:
                # Ouvre le fichier en mode lecture avec l'encodage utf-8
                with open(chemin_fichier, 'r', encoding='utf-8') as f:
                    # Charge le contenu JSON dans la variable donnees
                    donnees = json.load(f)
                # Parcourt chaque élément contenu dans les données JSON
                for item in donnees:
                    # Extrait l'expression textuelle de la fonction
                    expr_str = item.get("expression")
                    # Extrait la couleur ou utilise le bleu par défaut
                    couleur = item.get("couleur", "blue")
                    # Vérifie que l'expression textuelle n'est pas vide
                    if expr_str:
                        # Convertit la chaîne de texte en expression SymPy valide
                        expr = sp.sympify(expr_str)
                        # Crée un nouvel objet FonctionPrincipale
                        nouvelle_fonction = FonctionPrincipale(expr, couleur)
                        # Ajoute la fonction au modèle de la liste
                        self.editeurFonction.modele.add_item(nouvelle_fonction)
                # Affiche un message de succès dans la console
                print("Chargement du fichier JSON réussi !")
            # Capture les erreurs en cas de problème de lecture ou de format
            except Exception as e:
                # Affiche l'erreur détaillée dans la console
                print(f"Erreur lors du chargement du fichier JSON : {e}")

    # Charge la liste des fonctions depuis le dossier fichiersJSON au démarrage
    def charger_json_au_demarrage(self, chemin_fichier="fichiersJSON/fonctions.json"):
        # Appelle la méthode commune avec le fichier par défaut situé dans le dossier
        self.importer_donnees_json(chemin_fichier)

    # Sauvegarde la liste actuelle des fonctions dans le dossier fichiersJSON
    def sauvegarder_en_json(self, chemin_fichier="fichiersJSON/fonctions.json"):
        # Définit le nom du dossier cible pour les sauvegardes
        dossier = "fichiersJSON"
        # Vérifie si le dossier n'existe pas encore sur le disque
        if not os.path.exists(dossier):
            # Crée le dossier automatiquement s'il est absent
            os.makedirs(dossier)
        # Ouvre le fichier en mode écriture avec l'encodage utf-8
        with open(chemin_fichier, 'w', encoding='utf-8') as f:
            # Récupère les données formatées depuis le modèle de la liste
            donnees = self.editeurFonction.modele.to_json_data()
            # Écrit les données dans le fichier JSON avec une indentation de 4
            json.dump(donnees, f, indent=4, ensure_ascii=False)

    # Intercepte l'événement de fermeture de la fenêtre principale
    def closeEvent(self, event):
        # Sauvegarde automatiquement la liste dans le dossier en quittant l'application
        self.sauvegarder_en_json()
        # Accepte l'événement pour fermer la fenêtre normalement
        event.accept()

    # Ouvre l'explorateur pour sélectionner un fichier JSON manuellement
    def ouvrir_fichier_json(self):
        # Ouvre la boîte de dialogue de sélection de fichier et récupère le chemin
        chemin_fichier, _ = QFileDialog.getOpenFileName(
            self, "Ouvrir un fichier de fonctions JSON", "fichiersJSON", "Fichiers JSON (*.json);;Tous les fichiers (*)"
        )
        # Vérifie si l'utilisateur a bien sélectionné un fichier
        if chemin_fichier:
            # Appelle la méthode commune avec le fichier choisi par l'utilisateur
            self.importer_donnees_json(chemin_fichier)