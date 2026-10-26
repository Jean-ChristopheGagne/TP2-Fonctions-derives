import re
from PyQt6.QtWidgets import QDockWidget
from PyQt6.QtCore import QAbstractListModel, Qt, QModelIndex
from PyQt6.uic import loadUi

import fonction
from fonction import Fonction


class FenetreListFonction(QDockWidget):

    __fonction: list[Fonction]

    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("ui/listfonction.ui", self)
        self.__fonction = fonction

    def rowCount(self, parent=...):
        # retourner le nombre d'objets a afficher
        return len(self.__fonction)

    def data(self, index, role):
        # Il se peut que temporairement pendant un ajout ou une suppression l'index soit non valide...
        if not index.isValid() or not (0 <= index.row() < len(self.__fonction)):
            return None

        #récupérer l'objet a la row "index"
        molecule = self.__fonction[index.row()]

        #Pour chaque role décider ce qu'on doit afficher pour notre objet
        if role == Qt.ItemDataRole.DisplayRole:
            # Le texte clé à afficher directement à l'écran (souvent str)
            return str(fonction)

        if role == Qt.ItemDataRole.EditRole:
            # Le texte clé à afficher lorsqu'on edite l'élément (souvent str)
            return str(fonction)

        elif role == Qt.ItemDataRole.ToolTipRole:
            # Le texte de l'info-bulle qui apparaît lorsque l'utilisateur laisse sa souris immobile sur l'élément.
            return str(fonction)
        return None

    def add_item(self, item):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        #le code qui insère l'objet
        self.__fonction.append(item)
        self.endInsertRows()
        idx1 = self.index(0)
        idx2 = self.index(self.rowCount())
        self.dataChanged.emit(idx1, idx2, [Qt.ItemDataRole.DisplayRole])

    def remove_item(self, index: int):
        self.beginRemoveRows(QModelIndex(), self.rowCount(), self.rowCount())
        #le code qui supprime l'objet
        self.__fonction.pop(index)
        self.endRemoveRows()
        idx = self.index(index)
        self.dataChanged.emit(idx, idx, [Qt.ItemDataRole.DisplayRole])

     # Pour l'édition
    def flags(self, index):
        return super().flags(index) | Qt.ItemFlag.ItemIsEditable

    def setData(self, index, valeur, role=Qt.ItemDataRole.EditRole):
        if role == Qt.ItemDataRole.EditRole and valeur:
            s = str(valeur)
            m = re.fullmatch(r"\s*(.*?)\s*\((.*)\)\s*", s)
            if m:
                fonction = m.groups()
            else:
                fonction = s.strip(), "Not Defined"  # pas de parenthèses

            fx = self.__fonction[index.row()]
            fx.fonction = fonction
            self.dataChanged.emit(index, index, [role])
            return True
        return False