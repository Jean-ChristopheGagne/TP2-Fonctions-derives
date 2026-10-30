import sys
import traceback
from PyQt6.QtWidgets import QApplication
from fenetre_principale import FenetrePrincipale

# Crochet d'exception
def qt_exception_hook(exctype, value, tb):
    # Affiche l'erreur
    traceback.print_exception(exctype, value, tb)

# Point d'entrée
if __name__ == "__main__":
    # Redirige les erreurs
    sys.excepthook = qt_exception_hook
    # Crée l'app
    app = QApplication(sys.argv)
    # Instancie la fenêtre
    fenetre = FenetrePrincipale()
    # Affiche la fenêtre
    fenetre.show()
    # Quitte l'app
    sys.exit(app.exec())