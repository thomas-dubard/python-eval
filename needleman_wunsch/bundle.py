import argparse

# que l'on peut utiliser comme ceci
#message = "def"
#print(f"abc{red_text(message)}ghi")

parser = argparse.ArgumentParser()

parser.add_argument("dataset", help="Couples de fragments", type=list)

args = parser.parse_args()

swap = args.dataset
n = len(swap)

if n%2 == 1:
    raise TypeError("Il faut des couples de fragments")

liste = []
for k in range(n//2):
    liste.append(tuple(swap[2 * k], swap[2 * k + 1]))

for k in range(n//2):
    ruler = Ruler(*liste[k])
    ruler.compute()
    d = ruler.distance
    top, bottom = ruler.report()
    print(f"====== example # {k} - distance = {d}")
    print(top)
    print(bottom)