import grid
import boat
import bataille as bt
import joueur as jr
import sys
import numpy as np

def main():
    nbarg=0
    n=True
    ns=False
    if "--noShow" in sys.argv:
        nbarg+=1
        ns=True
    if "--aiOnly" in sys.argv:
        nbarg+=2
        if nbarg!=len(sys.argv)-1:
            print("CHeck number of arguments")
            exit()
        n=False
        if "--RandomAI" in sys.argv:
            j2=jr.RandomAI("A2")
        elif "--HeuristicAI" in sys.argv:
            j2=jr.HeuristicAI("A2")
        elif "--ProbabilisticAI":
            j2=jr.ProbabilistAI("A2")
        else:
            print("Unknown option")
            exit(1)
        b=bt.Bataille(jr.BrainDead(), j2)
        while b.tour(ns):
            pass
        print(j2.getNbCoup())
    else:
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
