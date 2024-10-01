import joueur as jr
import grid as gd

class Bataille:
    def __init__(self, j1, j2):
        self.js=[j1, j2]
        self.turn=0

    def tour(self, noShow):
        j=self.js[self.turn%2]
        j2=self.js[(self.turn+1)%2]
        coor=j.get_coor()
        if not noShow:
            if coor[0]==314:
                gd.affiche(j.getGrid())
                coor=(0,coor[1])
            if coor[1]==314:
                gd.affiche(j2.getGrid())
                coor=(coor[0],0)
        res=j2.attack(coor, j)
        if not noShow:
            if res==0:
                print("Rate !\n")
            elif res==1:
                print("Touche !\n")
            elif res in [2, 3]:
                print("Coule !\n")
        if res==3:
            return self.end(j, noShow)
        if not noShow:
            gd.affiche(j.getShots())
        self.turn+=1
        return 1

    def end(self, victor, noShow):
        if not noShow:
            print(f"{victor.getName()} a gagne")
        return 0
