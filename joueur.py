import grid as gd

class Joueur:
	def __init__(self):
		self.grille, self.b_list=gd.genere_grille()
	
	def get_coor(self):
		pass
	
class Human(Joueur):
	def __init__(self):
		super().__init__()
		#print(self.grille)
	
	def get_coor(self):
		x=int(input("x : "))
		y=int(input("y : "))
		return x, y

#a=Human()
#print(a.get_coor())
