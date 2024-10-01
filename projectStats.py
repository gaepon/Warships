from boat import Boat
import grid as gd

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

print(pl_possibles(5))
print(pl_possibles(4))
print(pl_possibles(3))
print(pl_possibles(2))
print(pl_possibles(1))
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

print(pl_possibles_liste(10, [5]))
print(pl_possibles_liste(10, [5, 1, 2]))
print(pl_possibles_liste(10, [4, 3]))

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

print(while_true(gd.genere_grille()))
