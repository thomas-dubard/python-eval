##Exercice 1

from needleman_wunsch.ruler import Ruler

# on crée un objet pour mesurer
# la distance entre deux chaines
ruler = Ruler("abcdefghi", "abcdfghi")

# on impose à l'utilisateur de la classe
# de lancer explicitement le calcul
ruler.compute()

# on obtient la distance
print(ruler.distance)

# et pour afficher les différences
top, bottom = ruler.report()
print(top)
print(bottom)