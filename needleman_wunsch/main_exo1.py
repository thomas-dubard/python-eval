##Exercice 1

from ruler import Ruler

# on crée un objet pour mesurer
# la distance entre deux chaines
rouler = Ruler("abcdefghi", "abcdfghi")

# on impose à l'utilisateur de la classe
# de lancer explicitement le calcul
rouler.compute()

# on obtient la distance
print(rouler.distance)

# et pour afficher les différences
top, bottom = rouler.report()
print(top)
print(bottom)