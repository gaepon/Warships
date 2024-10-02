import joueur as pl
import ui
import sys
from PySide6.QtWidgets import QApplication

def main():
    j=[pl.Human("Joueur1"), pl.Human("Joueur2")]
    app=QApplication()
    w=ui.GUI(j)
    w.show()
    sys.exit(app.exec())

if __name__=="__main__":
    main()
