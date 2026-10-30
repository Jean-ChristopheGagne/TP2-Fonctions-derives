from PyQt6.QtCore import QModelIndex, Qt, QAbstractListModel

from fonction_couple import FonctionCouple


class ListFonction(QAbstractListModel):

    # Liste des fonctions
    # Attribut fonctions
    __fonctions : list[FonctionCouple]

    # Init
    def __init__(self, fonctions=None):
        # Super init
        super().__init__()
        # Initialise liste
        self.__fonctions = fonctions if fonctions is not None else []

    # Row count
    def rowCount(self, parent=QModelIndex()):
        # Retourne longueur
        return len(self.__fonctions)

    # Data
    def data(self, index, role = Qt.ItemDataRole.DisplayRole):
        # Vérifie index
        if not index.isValid() or not (0 <= index.row() < len(self.__fonctions)):
            # Retourne None
            return None

        # Récupère objet
        fonction_obj = self.__fonctions[index.row()]

        # On retourne uniquement la chaîne de caractères brute de l'expression SymPy (ex: x**2)
        # Rôle affichage/édition
        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
            # Retourne str fonction
            return str(fonction_obj.fonction)

        # Rôle infobulle
        elif role == Qt.ItemDataRole.ToolTipRole:
            # Retourne couleur
            return f"Couleur: {fonction_obj.fonction_principale.couleur}"

        # Sinon None
        return None

    # Ajout item
    def add_item(self, item: FonctionCouple):
        # Début insertion
        self.beginInsertRows(QModelIndex(), len(self.__fonctions), len(self.__fonctions))
        # Ajoute
        self.__fonctions.append(item)
        # Fin insertion
        self.endInsertRows()

    # Supprime item
    def remove_item(self, index_row: int):
        # Vérifie index
        if 0 <= index_row < len(self.__fonctions):
            # Début suppression
            self.beginRemoveRows(QModelIndex(), index_row, index_row)
            # Retire
            self.__fonctions.pop(index_row)
            # Fin suppression
            self.endRemoveRows()

    # Flags
    def flags(self, index):
        # Retourne modifiable
        return super().flags(index) | Qt.ItemFlag.ItemIsEditable

    # Set data
    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        # Vérifie édition
        if role == Qt.ItemDataRole.EditRole and value and index.isValid():
            # Récupère item
            fx = self.__fonctions[index.row()]
            # Modifie fonction
            fx.fonction_principale = str(value)
            # Émet dataChanged
            self.dataChanged.emit(index, index, [role])
            # Succès
            return True
        # Échec
        return False