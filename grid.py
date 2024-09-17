from boat import Boat
from random import randint
from matplotlib import pyplot
import numpy as np

def peut_placer(grille:list[list[int]], coor:tuple[int], b_type:int, facing:str)->bool:
	y_length = len(grille)
	x_length = len(grille[0])
	
	if not (1<=b_type<=5):
		return False
	
	if 0<=coor[0]<x_length and 0<=coor[1]<y_length:
		if grille[coor[1]][coor[0]]!=0:
			return False
		i = 1
		b_length = b_type if b_type>=3 else b_type+1
		if facing == "h":
			while i<b_length:
				if coor[0]+i>=x_length:
					return False
				if grille[coor[1]][coor[0]+i]!=0:
					return False
				i += 1
			return True
			
		if facing == "v":
			while i<b_length:
				if coor[1]+i>=y_length:
					return False
				if grille[coor[1]+i][coor[0]]!=0:
					return False
				i += 1
			return True
	return False
		
		
def place(grille:list[list[int|Boat]], b_list:list[Boat], coor:tuple[int], b_type:int, facing:str)->list[list[int]]:
	if peut_placer(grille, coor, b_type, facing):
		b = Boat(coor, b_type, facing)
		b_list.append(b)
		grille[coor[1]][coor[0]]=5
		b_length = b_type if b_type>=3 else b_type+1
		if facing=="h":
			for i in range(b_length):
				grille[coor[1]][coor[0]+i]=b_type
		else:
			for i in range(b_length):
				grille[coor[1]+i][coor[0]]=b_type
		return grille
	return []
		
def remove(grille, b_list, b):
	#print("############# AVANT #############")
	#for l in grille:
	#	print(l)
	b_list.pop(b_list.index(b))
	b_length = b.type if b.type>=3 else b.type+1
	v=0
	h=1
	if b.facing=="v":
		v=1
		h=0
	for i in range(b_length):
		grille[b.coor[1]+i*v][b.coor[0]+i*h]=0
	#print("############# APRES #############")
	#for l in grille:
	#	print(l)
	return grille
	
def place_alea(grille:list[list[int]], b_type:int, b_list:list[Boat]):
	n_grille=[]
	while n_grille==[]:
		facing="h" if randint(0,1) else "v"
		n_grille=place(grille, b_list, (randint(0, len(grille[0])), randint(0, len(grille))), b_type, facing)
	return n_grille


def affiche(grille):
	pyplot.imshow(grille)
	pyplot.show()


def eq(g1, g2):
	return np.array_equiv(g1, g2)


def genere_grille():
	grille=[[0 for _ in range(10)] for __ in range(10)]
	b_list=[]
	for i in range(1, 6):
		place_alea(grille, i, b_list)
	return grille, b_list
