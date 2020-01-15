import argparse

# que l'on peut utiliser comme ceci
#message = "def"
#print(f"abc{red_text(message)}ghi")

parser = argparse.ArgumentParser()

parser.add_argument("dataset", help="Couples de fragments")

args = parser.parse_args()

texte = args.dataset

liste = []
for ligne in texte:


for k in range(n//2):
    ruler = Ruler(*liste[k])
    ruler.compute()
    d = ruler.distance
    top, bottom = ruler.report()
    print(f"====== example # {k} - distance = {d}")
    print(top)
    print(bottom)