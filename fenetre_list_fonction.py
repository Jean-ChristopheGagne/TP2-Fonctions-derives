import sympy as sp
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QDockWidget, QMessageBox
from PyQt6.uic import loadUi

from fonction_couple import FonctionCouple
from list_fonction import ListFonction

class FenetreListFonction(QDockWidget):

    # Définition du signal personnalisé
    fichiers_clique = pyqtSignal()

    # Init
    def __init__(self, parent=None):
        # Super init
        super().__init__(parent)
        # Charge ui
        loadUi("ui/listfonction.ui", self)

        # Instanciation du modèle de données
        # Crée modèle
        self.__modele = ListFonction()

        # Liaison du modèle au QListView
        # Assigne modèle vue
        self.fonctionListView.setModel(self.__modele)

        # Connexions des signaux aux slots
        # Connecte ajouter
        self.ajouter.clicked.connect(self.ajouter_fonction)
        # Connecte enlever
        self.enlever.clicked.connect(self.enlever_fonction)

        #Connexion du signal textChanged pour valider la saisie en temps réel
        # Connecte validation
        self.lineEdit.textChanged.connect(self.valider_saisie)

        #Désactiver le bouton Ajouter par défaut au démarrage (champ vide)
        # Désactive ajouter
        self.ajouter.setEnabled(False)

        # Connexion du bouton de ton interface UI au signal
        # Si bouton fichiers existe
        if hasattr(self, 'ajouterFichiers'):
            # Connecte signal
            self.ajouterFichiers.clicked.connect(self.emettre_signal_fichiers)

    # Propriété modèle
    @property
    def modele(self):
        """Expose le modèle pour pouvoir le lier au QComboBox de la fenêtre principale."""
        # Retourne modèle
        return self.__modele

        #Nouvelle méthode pour valider la saisie et gérer l'état du bouton/style
    # Valide saisie
    def valider_saisie(self, text):
        """Vérifie si le texte est une constante, un nombre ou une fonction valide."""
        # Nettoie texte
        texte = text.strip()
        # Si vide
        if not texte:
            # Style vide
            self.lineEdit.setStyleSheet("")
            # Désactive ajouter
            self.ajouter.setEnabled(False)
            return
        # Try parse
        try:
            #Valide aussi bien les constantes (ex: 3) que les expressions avec 'x'
            # Test sympify
            sp.sympify(texte)
            #Si valide, aucun fond rouge et bouton activé
            # Style normal
            self.lineEdit.setStyleSheet("")
            # Active ajouter
            self.ajouter.setEnabled(True)
        # Saisit erreur
        except Exception:
            #Si invalide, fond rouge clair et bouton désactivé
            # Style rouge
            self.lineEdit.setStyleSheet("background-color: #ffcccc;")
            # Désactive ajouter
            self.ajouter.setEnabled(False)

    # Valide et ajoute une fonction depuis l'input textuel
    def ajouter_fonction(self):
        # Récupère le texte directement depuis ton champ de saisie
        texte_saisi = self.lineEdit.text().strip()

        # Vérifie si le champ de texte est vide
        if not texte_saisi:
            return QMessageBox.warning(self, "Erreur", "Veuillez entrer une expression mathématique.")

        # Bloc try pour tester la validité mathématique
        try:
            contexte_autorise = {
                'cos': sp.cos, 'sin': sp.sin, 'tan': sp.tan,
                'sqrt': sp.sqrt, 'log': sp.log, 'exp': sp.exp,
                'x': sp.Symbol('x')
            }

            # Convertit en expression SymPy
            expr = sp.sympify(texte_saisi, locals=contexte_autorise)
            x_sym = sp.Symbol('x')

            # Vérifie si c'est un nombre constant ou si l'expression contient 'x'
            if not expr.is_number and x_sym not in expr.free_symbols:
                self.ajouter.setEnabled(False)
                return QMessageBox.warning(self, "Erreur","L'expression doit être un nombre constant ou contenir la variable 'x'.")

            # Si tout est valide, crée l'objet et l'ajoute à la liste
            nouvel_element = FonctionCouple(texte_saisi, couleur_f_princ="blue")
            self.modele.add_item(nouvel_element)

            # Vide le champ après l'ajout réussi
            self.lineEdit.clear()

        # Capture les erreurs si le texte n'a aucun sens mathématique
        except Exception as e:
            return QMessageBox.warning(self, "Erreur", f"Expression mathématique invalide : '{texte_saisi}'")

    # Enlève fonction
    def enlever_fonction(self):
        """Supprime la fonction actuellement sélectionnée dans la QListView."""
        # Récupère index
        index_selectionne = self.fonctionListView.currentIndex()
        # Si valide
        if index_selectionne.isValid():
            # Récupère ligne
            ligne = index_selectionne.row()
            # Retire item
            self.__modele.remove_item(ligne)

    # Émet signal
    def emettre_signal_fichiers(self):
        """Émet le signal personnalisé vers la fenêtre principale."""
        # Émet signal
        self.fichiers_clique.emit()