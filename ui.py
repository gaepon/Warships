import sys
import grid as gd
import joueur as pl
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QMainWindow, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Slot


def hex_to_color(code):
    ch=code.replace("#","")
    rgb=tuple(int(ch[i:i+2],16) for i in (0, 2, 4))
    return QColor.fromRgb(rgb[0], rgb[1], rgb[2])

class GridCase(QWidget):
    def __init__(self, x, y, mainWindow, clickable):
        super().__init__()
        self.x=x
        self.y=y
        self.clickable=clickable
        self.main=mainWindow
    
    def mousePressEvent(self, QMouseEvent):
        if self.underMouse() and self.clickable:
            w=self.parentWidget()
            if w:
                w.setGridCase(self.x, self.y, -1)
                color=w.getColorList()
                newColor=hex_to_color(color[0])
                p=self.palette()
                p.setColor(self.backgroundRole(), newColor)
                self.setPalette(p)
                self.main.nextWidget()

class GridWidget(QWidget):
    def __init__(self, grid, mainWindow, clickable=True):
        super().__init__()
        self.grille=grid
        self.setFixedSize(590,590)
        self.color = ["#050505","#101044","#F1C40F","#2ECC71","#F39C12","#E74C3C","#5B2C6F"]
        l = QGridLayout()
        
        l.setVerticalSpacing(1)
        l.setHorizontalSpacing(1)

        for i in range(10):
            for j in range(10):
                gc=GridCase(j, i, mainWindow, clickable)
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

class TurnScreen(QWidget):
	def __init__(self, text, p=None):
		super().__init__(parent=p)
		self.text=text
		
		l=QVBoxLayout(self)
		t=QLabel(parent=self)
		t.setText(self.text)
		t.setAlignment(Qt.AlignCenter)
		b=QPushButton("Next", parent=self)
		b.clicked.connect(self.parentWidget().nextWidget)
		
		l.addWidget(t)
		l.addWidget(b)
		self.setLayout(l)

class DualGrid(QWidget):
    def __init__(self, player, p=None):
        super().__init__(parent=p)
        shotGrid = player.getShots()
        boatGrid = player.getGrid()
        
        t1=QLabel()
        t2=QLabel()
        
        t1.setText("Your ships")
        t2.setText("Your shots")
        
        l=QGridLayout()
        l.addWidget(t1, 0, 0)
        l.addWidget(t2, 0, 1)
        l.addWidget(GridWidget(boatGrid, self.parentWidget(), False), 1, 0)
        l.addWidget(GridWidget(shotGrid, self.parentWidget()), 1, 1)
        
        self.setLayout(l)

class Screen(QWidget):
    def __init__(self, j1, j2, p=None):
        super().__init__(parent=p)
        
        self.i=0
        
        self.g1 = DualGrid(j1, p=self)
        self.ps1 = TurnScreen(j1.getName(), p=self)
        self.g2 = DualGrid(j2, p=self)
        self.ps2 = TurnScreen(j2.getName(), p=self)
        
        self.ps1.resize(1230, 620)
        self.ps2.resize(1230, 620)

        self.g1.hide()
        self.g2.hide()
        self.ps2.hide()
        self.ps1.show()

    @Slot()
    def nextWidget(self):
        self.i+=1
        widList=[self.ps1, self.g1, self.ps2, self.g2]
        widList[self.i%len(widList)].show()
        for y in range(len(widList)):
            if y!=self.i%len(widList):
                widList[y%len(widList)].hide()

class GUI(QMainWindow):
    def __init__(self, j1, j2):
        super().__init__()
        self.setFixedSize(1230,620)
        self.setWindowTitle("WARSHIPS !")
        
        w=Screen(j1, j2, p=self)
    
        self.setCentralWidget(w)


if __name__=="__main__":
    app=QApplication()
    j1=pl.Human("J1")
    j2=pl.Human("J2")
    w=GUI(j1, j2)
    w.show()
    sys.exit(app.exec())
