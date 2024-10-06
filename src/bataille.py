import joueur as jr
import grid as gd

class Bataille:
    """
    Represents a naval battle, is used in the terminal version
    """
    def __init__(self, j1, j2):
        self.js=[j1, j2]
        self.turn=0

    def tour(self, noShow:bool) -> int:
        """
        IN : bool
        OUT : int
        Plays a turn, returns 1 if the battle continues, 0 if it ended
        """
        j=self.js[self.turn%2]
        j2=self.js[(self.turn+1)%2]

        coor=j.get_coor()
        res=j2.attack(coor, j)

        self.showShotStatus(res, noShow)

        if res==3:
            return self.end(j, noShow)
        if not noShow:
            gd.affiche(j.getShots())
        self.turn+=1
        return 1

    def showShotStatus(self, res:int, noShow:bool) -> None:
        """
        IN : int, bool
        OUT : None
        Show if the show landed, or missed"""
        if not noShow:
            if res==0:
                print("Rate !\n")
            elif res==1:
                print("Touche !\n")
            elif res in [2, 3]:
                print("Coule !\n")

    def end(self, victor:jr.Joueur, noShow:bool) -> int:
        if not noShow:
            print(f"{victor.getName()} a gagne")
        return 0
