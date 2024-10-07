from boat import Boat
from random import random, randint
import grid as gd
import numpy as np

def pl_possibles(b_type, grille=[], taille_g=10):
	if grille==[]:
		grille=[[0 for _ in range(taille_g)] for __ in range(taille_g)]
	else:
		assert len(grille)==len(grille[0]), "Grille pas carrée"
		taille_g=len(grille)
	n=0
	for facing in ["v", "h"]:
		y=0
		while y<taille_g:
			x=0
			while x<taille_g:
				r=gd.peut_placer(grille, (x, y), b_type, facing)
				if r:
					n+=1
				x+=1
			y+=1
	return n
"""
print(pl_possibles(5))
print(pl_possibles(4))
print(pl_possibles(3))
print(pl_possibles(2))
print(pl_possibles(1))"""
#print(pl_possibles(1, [[0,0]]))

def pl_possibles_liste(taille_g, b_type_list):
	assert len(b_type_list)<=3, "Liste trop longue"

	grille=[[0 for _ in range(taille_g)] for __ in range(taille_g)]
	n=0
	b_temp=[]
	if len(b_type_list)==1:
		n+=pl_possibles(b_type_list[0], grille)
		
	elif len(b_type_list)==2:
		for facing in ["v", "h"]:
			x=0
			while x<taille_g:
				y=0
				while y<taille_g:
					g_temp=gd.place(grille, b_temp, (x, y), b_type_list[0], facing)
					if g_temp:
						n+=pl_possibles(b_type_list[-1], grille)
						grille=gd.remove(grille, b_temp, b_temp[0])
					y+=1
				x+=1
	
	else:
		x=[0,0]
		y=[0,0]
		for facing1 in ["v", "h"]:
			x[0]=0
			while x[0]<taille_g:
				y[0]=0
				while y[0]<taille_g:
					g_temp=gd.place(grille, b_temp, (x[0], y[0]), b_type_list[0], facing1)
					if g_temp!=[]:
						grille=g_temp
						for facing2 in ["v", "h"]:
							x[1]=0
							while x[1]<taille_g:
								y[1]=0
								while y[1]<taille_g:
									g_temp=gd.place(grille, b_temp, (x[1], y[1]), b_type_list[1], facing2)
									if g_temp!=[]:
										grille=g_temp
										n+=pl_possibles(b_type_list[-1], grille)
										grille=gd.remove(grille, b_temp, b_temp[1])
									y[1]+=1
								x[1]+=1
						grille=gd.remove(grille, b_temp, b_temp[0])
					y[0]+=1
				x[0]+=1
			
	return n

#print(pl_possibles_liste(10, [5]))
#print(pl_possibles_liste(10, [5, 1, 2]))
#print(pl_possibles_liste(10, [4, 3]))

def while_true(g1):
	power=0
	g2=gd.genere_grille()
	attempt=1
	while not gd.eq(g1, g2):
		if attempt==10**power:
			print(attempt)
			power+=1
		g2, b=gd.genere_grille()
		attempt+=1
	return attempt

#print(while_true(gd.genere_grille()))


def randomDetect(grid:list[list[int]], probaSensor:float, coor:tuple[int]) -> bool:
	if grid[coor[1]][coor[0]]!=0:
		return probaSensor>random()
	return False

def selectCoorGrid(probaGrid:list[list[float]]):
	ind=np.where(np.isclose(np.array(probaGrid), np.max(probaGrid)))
	return int(ind[1][0]), int(ind[0][0])

def bayeSearch(grid:list[list[int]], probaSensor:float, probaGrid=[])-> tuple:
	"""
	OUT : tuple[int], int
	Retourne les coordonnées de l'objet et le nombre de détections éffectuées
	"""
	assert len(grid)>0
	assert len(grid[0])>0

	n=1

	if probaGrid==[]:
		probaGrid=[[1/(len(grid)*len(grid[0])) for _ in range(len(grid[0]))] for __ in range(len(grid))]

	coor = selectCoorGrid(probaGrid)

	while not randomDetect(grid, probaSensor, coor):
		n+=1
		pi_k = probaGrid[coor[1]][coor[0]]
		for j in range(len(grid)):
			for i in range(len(grid[0])):
				pi_i = probaGrid[j][i]
				if i!=coor[0] or j!=coor[1]:
					probaGrid[j][i]=pi_i/(1-(probaSensor*pi_k))
				else :
					probaGrid[j][i]=((1-probaSensor)*pi_k)/(1-(probaSensor*pi_k))
		
		#print(coor)
		#print(np.sum(probaGrid))
		#print(np.array(probaGrid))
		coor = selectCoorGrid(probaGrid)
	
	return coor, n

print("small grid")
print(bayeSearch([[0, 0, 1], [0, 0, 0], [0, 0, 0]], 0.8))
print(bayeSearch([[0, 0, 1], [0, 0, 0], [0, 0, 0]], 0.1))

print("\n\nMedium grid")
medium_list = [[0 for _ in range(10)] for __ in range(10)]
x=randint(0, 9)
y=randint(0, 9)
medium_list[y][x]=1
print(f"1 placed in ({x}, {y})")
print(bayeSearch(medium_list, 0.8))
print(bayeSearch(medium_list, 0.5))
print(bayeSearch(medium_list, 0.1))

print("\n\nBig grid")
big_list = [[0 for _ in range(100)] for __ in range(100)]
x=randint(0, 99)
y=randint(0, 99)
big_list[y][x]=1
print(f"1 placed in ({x}, {y})")
print(bayeSearch(big_list, 0.8))
#print(bayeSearch(big_list, 0.5))
#print(bayeSearch(big_list, 0.1))
