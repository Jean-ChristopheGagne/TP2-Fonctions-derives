import sympy as sp
from PyQt6.QtWidgets import QDockWidget
from PyQt6.uic import loadUi

from fonction import Fonction
from list_fonction import ListFonction

class FenetreListFonction(QDockWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("ui/listfonction.ui", self)

        # Instanciation du modèle de données
        self.__modele = ListFonction()

        # Liaison du modèle au QListView
        self.fonctionListView.setModel(self.__modele)

        # Connexions des signaux aux slots
        self.ajouter.clicked.connect(self.ajouter_fonction)
        self.enlever.clicked.connect(self.enlever_fonction)

        #Connexion du signal textChanged pour valider la saisie en temps réel
        self.lineEdit.textChanged.connect(self.valider_saisie)
        #Désactiver le bouton Ajouter par défaut au démarrage (champ vide)
        self.ajouter.setEnabled(False)

    @property
    def modele(self):
        """Expose le modèle pour pouvoir le lier au QComboBox de la fenêtre principale."""
        return self.__modele

        #Nouvelle méthode pour valider la saisie et gérer l'état du bouton/style
    def valider_saisie(self, text):
        """Vérifie si le texte est une constante, un nombre ou une fonction valide."""
        texte = text.strip()
        if not texte:
            self.lineEdit.setStyleSheet("")
            self.ajouter.setEnabled(False)
            return
        try:
            #Valide aussi bien les constantes (ex: 3) que les expressions avec 'x'
            sp.sympify(texte)
            #Si valide, aucun fond rouge et bouton activé
            self.lineEdit.setStyleSheet("")
            self.ajouter.setEnabled(True)
        except Exception:
            #Si invalide, fond rouge clair et bouton désactivé
            self.lineEdit.setStyleSheet("background-color: #ffcccc;")
            self.ajouter.setEnabled(False)

    def ajouter_fonction(self):
        """Ajoute la fonction validée au modèle."""
        texte = self.lineEdit.text().strip()
        if not texte:
            return
        try:
            expr = sp.sympify(texte)
            nouvelle_fonction = Fonction(expr, "blue")
            self.__modele.add_item(nouvelle_fonction)
            self.lineEdit.clear()
            #Désactiver à nouveau le bouton après l'ajout réussi
            self.ajouter.setEnabled(False)
        except Exception as e:
            print(f"Erreur : {e}")

    def enlever_fonction(self):
        """Supprime la fonction actuellement sélectionnée dans la QListView."""
        index_selectionne = self.fonctionListView.currentIndex()
        if index_selectionne.isValid():
            ligne = index_selectionne.row()
            self.__modele.remove_item(ligne)