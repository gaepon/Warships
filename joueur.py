import grid as gd

class Joueur:
    def __init__(self, name):
        self.grille, self.b_list=gd.genere_grille()
        self.shots=[[0 for _ in range(10)] for ᄑ in range(10)]
        self.name=name
	
    def getCoor(self):
        pass

    def getShots(self):
        pass

    def getName(self):
        return self.name
	
class Human(Joueur):
    def __init__(self, name):
        super().__init__(name)
        #print(self.grille)
	
    def get_coor(self):
        x=int(input("x : "))
        y=int(input("y : "))
        return x, y

#a=Human()
#print(a.get_coor())
