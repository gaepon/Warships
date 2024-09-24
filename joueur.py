import grid as gd
import boat as bt

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
            j2.setShots(coor, 1)
            res=self.b_list[b_type-1].checkHealth(self.grille)
            if self.isDead():
                return 3
            return res
        else:
            j2.setShots(coor, -1)
            return 0
    
    def setShots(self, coor, val):
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
        x=int(input("x : "))
        y=int(input("y : "))
        return x, y
#a=Human("t")
#print(a.getName())

class RandomAI(Joueur):
    pass

class HeuristicAI(Joueur):
    pass
    
class ProbabilistAI(Joueur):
    pass
