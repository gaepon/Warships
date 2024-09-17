import grid
import boat

def main():
	grille, b_list=grid.genere_grille()
	for b in b_list:
		print(b)
	grille2, b_list2=grid.genere_grille()
	print("\nDeuxieme Liste")
	for b in b_list2:
		print(b)
	print(grid.eq(grille, grille))
	print(grid.eq(grille2, grille2))
	print(grid.eq(grille, grille2))
	grid.affiche(grille)

if __name__=="__main__":
	main()
