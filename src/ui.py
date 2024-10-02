import sys
import grid as gd
import numpy as np
import joueur as pl
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QMainWindow, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Slot


def hex_to_color(code):
    ch=code.replace("#","")
    rgb=tuple(int(ch[i:i+2],16) for i in (0, 2, 4))
    return QColor.fromRgb(rgb[0], rgb[1], rgb[2])

class GridCase(QWidget):
    def __init__(self, x:int, y:int, mainWindow, clickable:bool):
        super().__init__()
        self.x=x
        self.y=y
        self.clickable=clickable
        self.main=mainWindow
    
    def mousePressEvent(self, QMouseEvent) -> None:
        if self.underMouse() and self.clickable:
            w=self.parentWidget()
            if w:
                self.main.processTurn([self.x, self.y])
    
    def updateCase(self) -> None:
        w=self.parentWidget()
        if w:
            color=w.getColorList()
            newColor=hex_to_color(color[self.parentWidget().getGridCase(self.x, self.y)+1])
            p=self.palette()
            p.setColor(self.backgroundRole(), newColor)
            self.setPalette(p)
            self.update()

class GridWidget(QWidget):
    def __init__(self, grid:list[list[int]], mainWindow, clickable:bool=True):
        super().__init__()
        self.grille=grid
        self.setFixedSize(590,590)
        self.color = ["#050505","#101044","#F1C40F","#2ECC71","#F39C12","#E74C3C","#5B2C6F"]
        self.l = QGridLayout()
        
        self.l.setVerticalSpacing(1)
        self.l.setHorizontalSpacing(1)

        for i in range(10):
            for j in range(10):
                gc=GridCase(j, i, mainWindow, clickable)
                gc.setAutoFillBackground(True)
                set_color=hex_to_color(self.color[self.grille[i][j]+1])
                i_p = gc.palette()
                i_p.setColor(gc.backgroundRole(), set_color)
                gc.setPalette(i_p)
                self.l.addWidget(gc, i, j)
        
        self.setLayout(self.l)
    
    def getColorList(self) -> list[str]:
        return self.color
    
    def getGridCase(self, x:int, y:int) -> int:
        return self.grille[y][x]
    
    def updateGrid(self, ng):
        self.grille=ng

        for i in range(10):
            for j in range(10):
                self.l.itemAtPosition(i, j).widget().updateCase()

class TurnScreen(QWidget):
    def __init__(self, text:str, p:QWidget=None):
        super().__init__(parent=p)
        self.text=text
        self.label=QLabel(parent=self)
		
        l=QVBoxLayout(self)
        self.label.setText(self.text)
        self.label.setAlignment(Qt.AlignCenter)
        b=QPushButton("Next", parent=self)
        b.clicked.connect(self.parentWidget().nextWidget)
		
        l.addWidget(self.label)
        l.addWidget(b)
        self.setLayout(l)
    
    def setText(self, text:str) -> None:
        self.label.setText(text)

class DualGrid(QWidget):
    def __init__(self, player:pl.Joueur, mainWindow:QMainWindow, p=None):
        super().__init__(parent=p)
        self.p=player
        shotGrid = player.getShots()
        boatGrid = player.getGrid()
        self.grid1 = GridWidget(boatGrid, mainWindow, False)
        self.grid2 = GridWidget(shotGrid, mainWindow)
        
        t1=QLabel()
        t2=QLabel()
        
        t1.setText("Your ships")
        t2.setText("Your shots")
        
        l=QGridLayout()
        l.addWidget(t1, 0, 0)
        l.addWidget(t2, 0, 1)
        l.addWidget(self.grid1, 1, 0)
        l.addWidget(self.grid2, 1, 1)
        
        self.setLayout(l)
    
    def updateAll(self) -> None:
        self.grid1.updateGrid(self.p.getGrid())
        self.grid2.updateGrid(self.p.getShots())
    

class Screen(QWidget):
    def __init__(self, j1:pl.Joueur, j2:pl.Joueur, p=None):
        super().__init__(parent=p)
        
        self.i=0
        
        self.g1 = DualGrid(j1, p, p=self)
        self.ps1 = TurnScreen(j1.getName(), p=self)
        self.g2 = DualGrid(j2, p, p=self)
        self.ps2 = TurnScreen(j2.getName(), p=self)
        
        self.ps1.resize(1230, 620)
        self.ps2.resize(1230, 620)

        self.g1.hide()
        self.g2.hide()
        self.ps2.hide()
        self.ps1.show()

    @Slot()
    def nextWidget(self) -> None:
        self.i+=1
        widList=[self.ps1, self.g1, self.ps2, self.g2]
        widList[self.i%len(widList)].show()
        for y in range(len(widList)):
            if y!=self.i%len(widList):
                widList[y%len(widList)].hide()
    
    def getNextWidget(self) -> QWidget:
        widList=[self.ps1, self.g1, self.ps2, self.g2]
        return widList[(self.i+1)%len(widList)]

    def updateAll(self) -> None:
        self.g1.updateAll()
        self.g2.updateAll()
        self.update()

class EndScreen(QWidget):
    def __init__(self, text:str, app, p:QWidget=None):
        super().__init__(parent=p)
        self.label=QLabel(parent=self)
        self.app=app
		
        l=QVBoxLayout(self)
        self.label.setText(f"{text} won")
        self.label.setAlignment(Qt.AlignCenter)
        b=QPushButton("Close", parent=self)
        b.clicked.connect(self.closeWindow)
		
        l.addWidget(self.label)
        l.addWidget(b)
        self.setLayout(l)
    
    def closeWindow(self, app:QApplication) -> None:
        sys.exit()

class GUI(QMainWindow):
    def __init__(self, j:list[pl.Joueur], app):
        super().__init__()
        self.setFixedSize(1230,620)
        self.setWindowTitle("WARSHIPS !")
        self.turn=0
        self.j=j
        self.app=app

        self.w=Screen(j[0], j[1], p=self)
    
        self.setCentralWidget(self.w)
    
    def processTurn(self, coord:list[int]) -> None:
        j1=self.j[self.turn%2]
        j2=self.j[(self.turn+1)%2]
        res=j2.attack(coord, j1)
        ts=self.w.getNextWidget()
        if res==0:
            ts.setText("Miss")
        elif res==1:
            ts.setText("Hit")
        elif res==2:
            ts.setText("Sunk")
        elif res==3:
            self.setCentralWidget(EndScreen(j1.getName(), self.app))
        self.w.updateAll()
        self.w.nextWidget()
        self.turn+=1

if __name__=="__main__":
    app=QApplication()
    j1=pl.Human("J1")
    j2=pl.Human("J2")
    w=GUI([j1, j2], app)
    w.show()
    sys.exit(app.exec())
