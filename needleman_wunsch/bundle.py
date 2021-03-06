import argparse
from ruler import Ruler

parser = argparse.ArgumentParser()

parser.add_argument("dataset", help="Couples de fragments", type=str)

args = parser.parse_args()

texte = args.dataset

with open(texte, 'r') as fichier:
    """
    On extrait les chaînes à comparer d'un dataset au format txt.
    Cette méthode permet d'éviter la dernière ligne si en nombre impair.
    On groupe les chaînes à comparer par paires.
    """
    liste = []
    swap = []
    for ligne in fichier:
        if len(ligne) != 0:
            if len(swap) == 0:
                swap.append(ligne)
            else:
                liste.append((swap[0], ligne))
                swap = []

for k in range(len(liste)):
    ruler = Ruler(*liste[k])
    ruler.compute()
    d = ruler.distance
    top, bottom = ruler.report()
    print(f"====== example # {k} - distance = {d}")
    print(top)
    print(bottom)