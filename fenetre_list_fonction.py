import sympy as sp
from PyQt6.QtWidgets import QDockWidget
from PyQt6.uic import loadUi

from fonction import Fonction
from list_fonction import ListFonction


# Assurez-vous que c'est le bon nom de fichier pour votre classe ListFonction


class FenetreListFonction(QDockWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("ui/listfonction.ui", self)

        # Instanciation du modèle de données
        self.__modele = ListFonction()

        # Liaison du modèle au QListView (fonctionListView dans ton XML)
        self.fonctionListView.setModel(self.__modele)

        # Connexions des signaux aux slots
        self.ajouter.clicked.connect(self.ajouter_fonction)
        self.enlever.clicked.connect(self.enlever_fonction)

        #Liaison du modèle à la QListView présente dans ton fichier .ui
        if hasattr(self, "listView"):
            self.listView.setModel(self.__modele)

    @property
    def modele(self):
        """Expose le modèle pour pouvoir le lier au QComboBox de la fenêtre principale."""
        return self.__modele

    def ajouter_fonction(self):
        """Valide l'expression SymPy, colore si invalide, et ajoute au modèle."""
        texte = self.lineEdit.text().strip()

        if not texte:
            return

        try:
            # 1. Validation avec SymPy
            expr = sp.sympify(texte)

            # 2. Création de l'objet Fonction (par exemple avec la couleur bleue par défaut)
            nouvelle_fonction = Fonction(expr, "blue", 0.0, 10.0)

            # 3. Ajout dans le modèle (ce qui met à jour la QListView et le QComboBox)
            self.__modele.add_item(nouvelle_fonction)

            # 4. Réinitialisation du champ et du style
            self.lineEdit.clear()
            self.lineEdit.setStyleSheet("")

        except Exception as e:
            # Si l'expression est invalide : fond rouge clair
            self.lineEdit.setStyleSheet("background-color: #ffcccc;")
            print(f"Expression invalide : {e}")

    def enlever_fonction(self):
        """Supprime la fonction actuellement sélectionnée dans la QListView."""
        index_selectionne = self.fonctionListView.currentIndex()
        if index_selectionne.isValid():
            ligne = index_selectionne.row()
            self.__modele.remove_item(ligne)