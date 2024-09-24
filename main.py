import grid
import boat
import bataille as bt
import joueur as jr

def main():
    n=True
    while n:
        print("Choose your enemy :\n1:Human, 2:Random, 3:Heuristic, 4:Probabilist")
        a=input("Your choice : ")
        if a=="1":
            j2=jr.Human("Joueur2")
            n=False
        elif a=="2":
            j2=jr.RandomAI()
            n=False
        elif a=="3":
            j2=jr.HeuristicAI("Joueur2")
            n=False
        elif a=="4":
            j2=jr.ProbabilistAI("Joueur2")
            n=False
    b=bt.Bataille(jr.Human("Joueur1"), j2)
    while b.tour():
        pass
    exit(0)

if __name__=="__main__":
	main()
