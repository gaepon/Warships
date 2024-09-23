import sys
import grid as gd
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QMainWindow

def printMat(mat):
    for l in mat:
        print(l)

def hex_to_color(code):
    ch=code.replace("#","")
    rgb=tuple(int(ch[i:i+2],16) for i in (0, 2, 4))
    return QColor.fromRgb(rgb[0], rgb[1], rgb[2])

class GridCase(QWidget):
    def __init__(self, x, y):
        super().__init__()
        self.x=x
        self.y=y
    
    def mousePressEvent(self, QMouseEvent):
        if self.underMouse():
            w=self.parentWidget()
            if w:
                w.setGridCase(self.x, self.y, -1)
                color=w.getColorList()
                newColor=hex_to_color(color[0])
                p=self.palette()
                p.setColor(self.backgroundRole(), newColor)
                self.setPalette(p)

class GridWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.grille, self.b_list = gd.genere_grille()
        self.color = ["#050505","#101044","#F1C40F","#2ECC71","#F39C12","#E74C3C","#5B2C6F"]
        l = QGridLayout()
        
        l.setVerticalSpacing(1)
        l.setHorizontalSpacing(1)

        for i in range(10):
            for j in range(10):
                gc=GridCase(j, i)
                gc.setAutoFillBackground(True)
                set_color=hex_to_color(self.color[self.grille[i][j]+1])
                i_p = gc.palette()
                i_p.setColor(gc.backgroundRole(), set_color)
                gc.setPalette(i_p)
                l.addWidget(gc, i, j)
        
        self.setLayout(l)
    
    def getColorList(self):
        return self.color
    
    def setGridCase(self, x, y, val):
        self.grille[y][x]=val

class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(600,600)
        self.setWindowTitle("WARSHIPS !")

        w = GridWidget()

        self.setCentralWidget(w)

app=QApplication()
w=GUI()
w.show()
sys.exit(app.exec())
