import grid as gd
import boat as bt
from random import randint
import numpy as np
from enum import Enum

"""
HITSTATES :
    SUNK = 2
    HIT = 1
    MISS = -1
    UNKNOWN = 0
"""
    
class Joueur:
    """
    Represents a player, has empty methods
    """
    def __init__(self, name):
        self.grille, self.b_list=gd.genere_grille()
        self.shots=[[0 for _ in range(10)] for ᄑ in range(10)]
        self.name=name
        self.nb_coup=0
	
    def getCoor(self) -> tuple[int]:
        """
        Get target coordinates
        """
        pass
    
    def getNbCoup(self) -> int:
        """
        Get how many turn this player played
        """
        return self.nb_coup

    def getGrid(self) -> list[list[int]]:
        """
        Get the ships grid
        """
        return self.grille

    def getShots(self) -> list[list[int]]:
        """
        Get the past shots grid
        """
        return self.shots
    
    def setShots(self, x:int, y:int, val:int):
        """
        Set the value of (x, y) in the shots grid
        """
        self.shots[y][x]=val

    def getName(self):
        """
        What is your name ?
        (What is your quest ?)
        (What is your favourite color ?)
        """
        return self.name
    
    def someoneGotSunk(self, boat : bt.Boat) -> None:
        """
        Sets a boat in the shots grid at 2, to indicate that it's sunk
        """
        v=0
        h=1
        if boat.getFacing()=="v":
            v=1
            h=0
        
        x, y = boat.get_coor()
        b_length = boat.get_b_type() if boat.get_b_type()>=3 else boat.get_b_type()+1

        for i in range(b_length):
            self.shots[y+i*v][x+i*h]=2

    def attack(self, coor:tuple[int], j2):
        """
        IN : tuple[int], Joueur
        Out : int
        self gets attacked by j2 in coor, the function returns:
        0 if it's a miss
        1 if it's a hit
        2 if the boat is sunk
        3 if self lost
        """
        if self.grille[coor[1]][coor[0]]!=0:
            b_type=self.grille[coor[1]][coor[0]]
            self.grille[coor[1]][coor[0]]=-1
            res=self.b_list[b_type-1].checkHealth(self.grille)
            if res==2:
                j2.someoneGotSunk(self.b_list[b_type-1])
            else:
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
        for b in self.b_list:
            if b.getDeath()==0:
                return 0
        return 1

class Human(Joueur):
    def __init__(self, name):
        super().__init__(name)
	
    def get_coor(self):
        x=-1
        y=-1
        while not(0<=x<len(self.grille[0])):
            x=int(input("x : "))
        while not(0<=y<len(self.grille)):
            y=int(input("y : "))
        self.nb_coup+=1
        return x, y

class RandomAI(Joueur):
    def __init__(self, name):
        super().__init__(name)
    
    def get_coor(self):
        max_x=len(self.grille[0])
        max_y=len(self.grille)
        c=1
        while c!=0:
            x=randint(0, max_x-1)
            y=randint(0, max_y-1)
            c=self.shots[y][x]
        self.nb_coup+=1
        return x, y


class HeuristicAI(Joueur):
    def __init__(self, name):
        super().__init__(name)
        self.hits=[]
    
    def get_coor(self):
        max_x=len(self.grille[0])
        max_y=len(self.grille)
        x=-1
        y=-1
        ncoor=False

        if self.hits!=[]:
            while (not(0<=x<max_x) or not(0<=y<max_y)):
                if len(self.hits)==0:
                    ncoor=True 
                x, y=self.hits.pop()
        if self.hits==[] or ncoor:
            c=1
            while c!=0:
                x=randint(0, max_x-1)
                y=randint(0, max_y-1)
                c=self.shots[y][x]
        self.nb_coup+=1
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
    
    
class ProbabilistAI(Joueur):
    def __init__(self, name):
        super().__init__(name)
        self.targets = [1,2,3,4,5]
        
    def calcPosPos(self, b_type):
        posPos=[[0 for _ in range(10)] for ₙ in range(10)]
        for facing in ["v", "h"]:
            v=0
            h=1
            if facing=="v":
                v=1
                h=0
            y=0
            while y<10:
                x=0
                while x<10:
                    if self.peut_placer(self.shots, (x, y), b_type, facing):
                        b_length = b_type if b_type>=3 else b_type+1
                        for i in range(b_length):
                            if self.shots[y+i*v][x+i*h]==0:
                                c=0
                                if self.nextToHit((x+i*h, y+i*v)):
                                    c=10
                                posPos[y+i*v][x+i*h]+=1+c
                    x+=1
                y+=1
        return posPos
    
    def nextToHit(self, coor):
        coords=[]
        for i in [-1, 1]:
            if 0<=coor[1]+i<len(self.shots) and self.shots[coor[1]+i][coor[0]]==0:
                coords.append((coor[0], coor[1]+i))
        for j in [-1, 1]:
            if 0<=coor[0]+j<len(self.shots[0]) and self.shots[coor[1]][coor[0]+j]==0:
                coords.append((coor[0]+j, coor[1]))
        for c in coords:
            if self.shots[c[1]][c[0]]==1:
                return True

    def peut_placer(self, grille:list[list[int]], coor:tuple[int], b_type:int, facing:str)->bool:
        y_length = len(grille)
        x_length = len(grille[0])
	
        if not (1<=b_type<=5):
            return False

        if 0<=coor[0]<x_length and 0<=coor[1]<y_length:
            if grille[coor[1]][coor[0]]==-1 or grille[coor[1]][coor[0]]==2:
                return False
            i = 1
            v=0
            h=1
            if facing=="v":
                v=1
                h=0
            b_length = b_type if b_type>=3 else b_type+1
            for i in range(b_length):
                if coor[0]+i*h>=x_length or coor[1]+i*v>=y_length:
                    return False
                case = grille[coor[1]+i*v][coor[0]+i*h]
                if case==-1 or case==2:
                    return False

            return True
        return False
    
    def someoneGotSunk(self, boat : bt.Boat):
        super().someoneGotSunk(boat)
        self.targets.pop(self.targets.index(boat.get_b_type()))

    def get_coor(self):
        posPos = [[0 for _ in range(10)] for ᖙ in range(10)]
        for i in self.targets:
            posPos = np.add(posPos, self.calcPosPos(i))
        #print("posPos : ", np.array(posPos))
        ind = np.where(np.array(posPos) == np.max(posPos))
        self.nb_coup+=1
        return int(ind[1][0]), int(ind[0][0])

class BrainDead(Joueur):
    def __init__(self):
        super().__init__("Bob")
    
    def get_coor(self):
        return 0, 0

if __name__=="__main__":
    m=np.array([[0,-1,-1,0,-1,0,0,-1,-1,0],[-1,-1,0,-1,2,2,2,-1,0,-1],[-1,0,-1,2,0,-1,-1,0,-1,0],[0,-1,0,2,-1,2,0,-1,-1,0],[-1,-1,0,2,-1 ,2,-1 ,1 ,0,-1],[-1 ,0,-1, 2,-1 , 2 , 0 , 0 ,-1 , 0],[ 0 ,-1 , 0 , 2 , 0 , 2 ,-1 , 0 , 0 ,-1],[-1 ,-1,  0,  0, -1,  0,  0, -1,  0,  0],[ 0 , 0 ,-1,  0,  0, -1,  0,  0, -1,  0],[ 1,  1,  0, -1,  0,  0, -1,  0,  0, -1]])
    j1=ProbabilistAI("TestAI")
    print(j1.peut_placer(m, (0, 9), 3, "h"))
    print(j1.peut_placer(m, (0, 9), 2, "h"))
    print(j1.peut_placer(m, (0, 9), 1, "h"))