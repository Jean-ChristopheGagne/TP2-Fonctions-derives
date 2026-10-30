from typing import override

from PyQt6.QtCore import QModelIndex, Qt, QAbstractListModel

from fonction import Fonction
from fonction_couple import FonctionCouple


class ListFonction(QAbstractListModel):

    # Liste des fonctions
    __fonctions : list[FonctionCouple]

    # Conctructeur de la classe
    def __init__(self, fonctions=None):
        super().__init__()
        self.__fonctions = fonctions if fonctions is not None else []

    @override
    def rowCount(self, parent=QModelIndex()):
        return len(self.__fonctions)

    @override
    def data(self, index, role = Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.__fonctions)):
            return None

        fonction_obj = self.__fonctions[index.row()]

        # On retourne uniquement la chaîne de caractères brute de l'expression SymPy (ex: x**2)
        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
            return str(fonction_obj.fonction_principale.fonction)

        elif role == Qt.ItemDataRole.ToolTipRole:
            return f"Couleur: {fonction_obj.fonction_principale.couleur}"

        return None

    def add_item(self, item: FonctionCouple):
        self.beginInsertRows(QModelIndex(), len(self.__fonctions), len(self.__fonctions))
        self.__fonctions.append(item)
        self.endInsertRows()

    def remove_item(self, index_row: int):
        if 0 <= index_row < len(self.__fonctions):
            self.beginRemoveRows(QModelIndex(), index_row, index_row)
            self.__fonctions.pop(index_row)
            self.endRemoveRows()

    @override
    def flags(self, index):
        return super().flags(index) | Qt.ItemFlag.ItemIsEditable

    @override
    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        if role == Qt.ItemDataRole.EditRole and value and index.isValid():
            fx = self.__fonctions[index.row()]
            fx.fonction_principale = str(value)
            self.dataChanged.emit(index, index, [role])
            return True
        return False