import joueur as jr

class Bataille:
	def __init__(self, j1, j2):
		self.js=[j1, j2]
        self.turn=0

    def tour(self):
        j=self.js[self.turn%2]
        pos=j.get_coor()
        res=self.js[(self.turn+1)%2].attack(coor)
        if res==0:
            print("Rate !\n")
        elif res==1:
            print("Touche !\n")
        elif:
            print("Coule !\n")
        else:
            print("Coule !\n")
            return self.end(j)
        j.getShots().affiche()
        self.turn+=1
        return 1

    def end(self, victor):
        print(f"{j.getName()} a gagne")
        return 0
