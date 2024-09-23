import sys
import grid as gd
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication, QWidget, QGridLayout

def hex_to_color(code):
    ch=code.replace("#","")
    rgb=tuple(int(ch[i:i+2],16) for i in (0, 2, 4))
    return QColor.fromRgb(rgb[0], rgb[1], rgb[2])

class GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(600,600)
        bt_color = ["#101080","#000064","#F1C40F","#2ECC71","#F39C12","#E74C3C","#5B2C6F"]

        grille, b_list = gd.genere_grille()

        l = QGridLayout()

        for i in range(10):
            for j in range(10):
                itemcolor=QWidget()
                itemcolor.setAutoFillBackground(True)
                set_color=hex_to_color(bt_color[grille[i][j]+1])
                i_p = itemcolor.palette()
                i_p.setColor(itemcolor.backgroundRole(), set_color)
                itemcolor.setPalette(i_p)
                l.addWidget(itemcolor, i, j)

        self.setLayout(l)

app=QApplication()
w=GUI()
w.show()
sys.exit(app.exec())
