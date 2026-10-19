import sys
import traceback

from PyQt6.QtWidgets import QApplication

from fenetre_principale import FenetrePrincipale

def qt_exception_hook(exctype, value, tb):
    traceback.print_exception(exctype, value, tb)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = FenetrePrincipale()
    fenetre.show()
    sys.exit(app.exec())