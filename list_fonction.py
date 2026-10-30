from PyQt6.QtCore import QModelIndex, Qt, QAbstractListModel

from fonction import Fonction


class ListFonction(QAbstractListModel):
    def __init__(self, fonctions=None):
        super().__init__()
        self.__fonctions = fonctions if fonctions is not None else []

    def rowCount(self, parent=QModelIndex()):
        return len(self.__fonctions)

    def data(self, index, role):
        if not index.isValid() or not (0 <= index.row() < len(self.__fonctions)):
            return None

        fonction_obj = self.__fonctions[index.row()]

        # On retourne uniquement la chaîne de caractères brute de l'expression SymPy (ex: x**2)
        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
            return str(fonction_obj.fonction)

        elif role == Qt.ItemDataRole.ToolTipRole:
            return f"Couleur: {fonction_obj.couleur}"

        return None

    def add_item(self, item: Fonction):
        self.beginInsertRows(QModelIndex(), len(self.__fonctions), len(self.__fonctions))
        self.__fonctions.append(item)
        self.endInsertRows()

    def remove_item(self, index_row: int):
        if 0 <= index_row < len(self.__fonctions):
            self.beginRemoveRows(QModelIndex(), index_row, index_row)
            self.__fonctions.pop(index_row)
            self.endRemoveRows()

    def flags(self, index):
        return super().flags(index) | Qt.ItemFlag.ItemIsEditable

    def setData(self, index, valeur, role=Qt.ItemDataRole.EditRole):
        if role == Qt.ItemDataRole.EditRole and valeur and index.isValid():
            fx = self.__fonctions[index.row()]
            fx.fonction = str(valeur)
            self.dataChanged.emit(index, index, [role])
            return True
        return False