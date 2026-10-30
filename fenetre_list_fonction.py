import sympy as sp
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QDockWidget
from PyQt6.uic import loadUi

from fonction_principale import FonctionPrincipale
from list_fonction import ListFonction

class FenetreListFonction(QDockWidget):

    # Définition du signal personnalisé
    # Signal fichiers
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

    # Ajoute fonction
    def ajouter_fonction(self):
        # Récupère texte
        texte = self.lineEdit.text().strip()
        # Si vide
        if not texte:
            return

        # Try ajout
        try:
            # Sympify
            expr = sp.sympify(texte)
            # Crée fonction
            nouvelle_fonction = FonctionPrincipale(expr, "blue")
            # Ajoute au modèle
            self.__modele.add_item(nouvelle_fonction)
            # Vide lineEdit
            self.lineEdit.clear()
            # Désactiver à nouveau le bouton après l'ajout réussi
            # Désactive ajouter
            self.ajouter.setEnabled(False)
        # Saisit erreur
        except Exception as e:
            # Affiche erreur
            print(f"Erreur : {e}")

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