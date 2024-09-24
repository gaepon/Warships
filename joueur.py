import grid as gd
import boat as bt
from random import randint

class Joueur:
    def __init__(self, name):
        self.grille, self.b_list=gd.genere_grille()
        self.shots=[[0 for _ in range(10)] for ᄑ in range(10)]
        self.name=name
	
    def getCoor(self):
        pass
    
    def getGrid(self):
        return self.grille

    def getShots(self):
        return self.shots
    
    def setShots(self, x, y, val):
        self.shots[y][x]=val

    def getName(self):
        return self.name
    
    def attack(self, coor, j2):
        if self.grille[coor[1]][coor[0]]!=0:
            b_type=self.grille[coor[1]][coor[0]]
            self.grille[coor[1]][coor[0]]=-1
            res=self.b_list[b_type-1].checkHealth(self.grille)
            j2.setShots(coor, 1, res)
            if self.isDead():
                return 3
            return res
        else:
            j2.setShots(coor, -1, 0)
            return 0
    
    def setShots(self, coor, val, res):
        self.shots[coor[1]][coor[0]]=val

    def isDead(self):
        for i in range(len(self.b_list)):
            if self.b_list[i].getDeath()==0:
                return 0
        return 1

class Human(Joueur):
    def __init__(self, name):
        super().__init__(name)
        #print(self.grille)
	
    def get_coor(self):
        x=-1
        y=-1
        while not(0<=x<len(self.grille[0])) and x!=314:
            x=int(input("x : "))
        while not(0<=y<len(self.grille)) and y!=314:
            y=int(input("y : "))
        return x, y
#a=Human("t")
#print(a.getName())

class RandomAI(Joueur):
    pass

class HeuristicAI(Joueur):
    def __init__(self, name):
        super().__init__(name)
        self.hits=[]
    
    def get_coor(self):
        max_x=len(self.grille[0])
        max_y=len(self.grille)
        if self.hits==[]:
            c=-1
            while c==-1:
                x=randint(0, max_x-1)
                y=randint(0, max_y-1)
                c=self.shots[y][x]
        else:
            x=-1
            y=-1
            while not(0<=x<max_x) or not(0<=y<max_y): 
                x, y=self.hits.pop()
        return x, y
    
    def setShots(self, coor, val, res):
        self.shots[coor[1]][coor[0]]=val
        if res==1:
            for i in [-1, 1]:
                if 0<=coor[1]+i<len(self.shots) and self.shots[coor[1]+i][coor[0]]==0:
                    self.hits.append((coor[0], coor[1]+i))
            for j in [-1, 1]:
                if 0<=coor[0]+j<len(self.shots[0]) and self.shots[coor[1]][coor[0]+j]==0:
                    self.hits.append((coor[0]+j, coor[1]))
            print(self.hits, coor)
    
class ProbabilistAI(Joueur):
    pass
