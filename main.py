import grid
import boat
import bataille as bt
import joueur as jr

def main():
    b=bt.Bataille(jr.Human("Joueur1"), jr.Human("Joueur2"))
    while b.tour():
        pass
    exit(0)

if __name__=="__main__":
	main()
