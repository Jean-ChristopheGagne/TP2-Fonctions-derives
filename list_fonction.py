from typing import override

from PyQt6.QtCore import QModelIndex, Qt, QAbstractListModel

from fonction_couple import FonctionCouple
from fonction_principale import FonctionPrincipale


class ListFonction(QAbstractListModel):

    # Liste des fonctions
    __fonctions : list[FonctionCouple]

    # Constructeur
    def __init__(self, fonctions=None):
        super().__init__()
        self.__fonctions = fonctions if fonctions is not None else []

    @override
    # Nombre de lignes
    def rowCount(self, parent=QModelIndex()):
        return len(self.__fonctions)

    @override
    # Données de la cellule
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.__fonctions)):
            return None

        fonction_obj = self.__fonctions[index.row()]

        # On retourne uniquement la chaîne de caractères brute de l'expression SymPy via fonction_principale
        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
            if hasattr(fonction_obj, 'fonction_principale') and fonction_obj.fonction_principale:
                return str(fonction_obj.fonction_principale.fonction)
            return ""

        elif role == Qt.ItemDataRole.ToolTipRole:
            # Récupère directement la couleur de la fonction principale
            if hasattr(fonction_obj, 'fonction_principale') and fonction_obj.fonction_principale:
                return f"Couleur: {fonction_obj.fonction_principale.couleur}"
            return "Couleur: blue"

        return None

    # Ajout d'un élément
    def add_item(self, item: FonctionCouple):
        self.beginInsertRows(QModelIndex(), len(self.__fonctions), len(self.__fonctions))
        self.__fonctions.append(item)
        self.endInsertRows()

    # Suppression d'un élément
    def remove_item(self, index_row: int):
        if 0 <= index_row < len(self.__fonctions):
            self.beginRemoveRows(QModelIndex(), index_row, index_row)
            self.__fonctions.pop(index_row)
            self.endRemoveRows()

    @override
    # Drapeaux des éléments
    def flags(self, index):
        return super().flags(index) | Qt.ItemFlag.ItemIsEditable

    @override
    # Modification d'une donnée
    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        if role == Qt.ItemDataRole.EditRole and value and index.isValid():
            fx = self.__fonctions[index.row()]
            try:
                # Met à jour l'expression de la fonction principale via le constructeur d'expression
                new_expr = FonctionCouple.definir_fonction_principale(str(value))
                fx.fonction_principale = FonctionPrincipale(new_expr, fx.fonction_principale.couleur)
                self.dataChanged.emit(index, index, [role])
                return True
            except Exception:
                return False
        return False

    # Récupère un élément par son index
    def get_item(self, index_row: int) -> FonctionCouple | None:
        if 0 <= index_row < len(self.__fonctions):
            return self.__fonctions[index_row]
        return None

    # Convertit la liste des fonctions en dictionnaires pour le JSON
    def to_json_data(self) -> list[dict]:
        data = []
        # On parcourt directement la liste interne sans vérification complexe
        for fx in self.__fonctions:
            try:
                if hasattr(fx,'fonction_principale') and fx.fonction_principale and fx.fonction_principale.fonction is not None:
                    data.append({
                        "expression": str(fx.fonction_principale.fonction),
                        "couleur": fx.fonction_principale.couleur
                        if hasattr(fx.fonction_principale,'couleur') else "blue"
                    })
            except Exception as e:
                print(f"Erreur lors de la conversion d'un élément pour le JSON : {e}")
        return data