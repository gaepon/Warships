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
    
    def someoneGotSunk(self, boat : bt.Boat):
        v=0
        h=1
        if boat.getFacing()=="v":
            v=1
            h=0
        x, y = boat.get_coor()
        b_length = boat.get_b_type() if boat.get_b_type()>=3 else boat.get_b_type()+1
        for i in range(b_length):
            self.shots[y+i*v][x+i*h]=2

    def attack(self, coor, j2):
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
    def __init__(self, name):
        super().__init__(name)
    
    def get_coor(self):
        max_x=len(self.grille[0])
        max_y=len(self.grille)
        c=0
        while c!=0:
            x=randint(0, max_x-1)
            y=randint(0, max_y-1)
            c=self.shots[y][x]
        return x, y


class HeuristicAI(Joueur):
    def __init__(self, name):
        super().__init__(name)
        self.hits=[]
    
    def get_coor(self):
        max_x=len(self.grille[0])
        max_y=len(self.grille)
        if self.hits==[]:
            c=0
            while c!=0:
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
            if grille[coor[1]][coor[0]]!=0:
                return False
            i = 1
            v=0
            h=1
            if facing=="v":
                v=1
                h=0
            b_length = b_type if b_type>=3 else b_type+1
            while i<b_length:
                if coor[0]+i*h>=x_length or coor[1]+i*v>=y_length:
                    return False
                case = grille[coor[1]+i*v][coor[0]+i*h]
                if case==-1 or case==2:
                    return False
                i += 1
            return True
        return False
    
    def someoneGotSunk(self, boat : bt.Boat):
            v=0
            h=1
            if boat.getFacing()=="v":
                v=1
                h=0
            x, y = boat.get_coor()
            self.targets.pop(self.targets.index(boat.get_b_type()))
            b_length = boat.get_b_type() if boat.get_b_type()>=3 else boat.get_b_type()+1
            for i in range(b_length):
                self.shots[y+i*v][x+i*h]=2

    def get_coor(self):
        posPos = [[0 for _ in range(10)] for ᖙ in range(10)]
        for i in self.targets:
            posPos = np.add(posPos, self.calcPosPos(i))
        print(np.array(posPos))
        ind = np.where(np.array(posPos) == np.max(posPos))
        print(ind[0][0], ind[1][0], " | max : ", np.max(posPos))
        return ind[1][0], ind[0][0]
