import numpy as np
from colorama import init, Fore, Style

# Variable à changer pour adapter les scores
egalite = 1
trou = 1

def red_text(text: str) -> str:
    """
    On utilise cette fonction pour proprement inclure du texte en rouge.
    """
    init(convert=True) # nécessaire sous des OS propriétaires :p
    return f"{Fore.RED}{text}{Style.RESET_ALL}"

class Ruler:
    """
    Cette classe vise à permettre de comparer deux chaînes de caractères.
    On va construire une matrice de comparaison mat.
    Puis on va l'utiliser pour calculer la distance entre ces chaînes.
    """
    def __init__(self, str1, str2):
        self._alignA = ""
        self._alignB = ""
        self.A = " " + str1
        self.B = " " + str2
        # Oui je triche car sinon le premier caractère est ignoré...
        # Mais grâce à ça ça marche et puis ça ne change pas la distance ...

        #Initialisation des properties
        nb_col = len(self.B)
        nb_ligne = len(self.A)
        self._mat = np.array([[0]*(nb_col+1)]*(nb_ligne+1))
        self.distance = None

    def compute(self):
        """
        Cette fonction remplit la matrice de comparaison.
        Elle est basée sur l'algorithme de Needleman-Wunsch.
        """
        for i in range(len(self.A)):
            self.mat[i][0] = 1 * i
        for j in range(len(self.B)):
            self.mat[0][j] = 1 * j
        for i in range(1, len(self.A)):
            for j in range(1, len(self.B)):
                if self.A[i] == self.B[j]:
                    # Même caractère
                    s1 = self.mat[i - 1][j - 1] - 1
                else:
                    # Caractère différent
                    s1 = self.mat[i - 1][j - 1] + 1
                # Il manque un caractère
                s2 = self.mat[i][j - 1] + 1
                # Il faut insérer un caractère
                s3 = self.mat[i - 1][j] + 1
                # On identifie la situation dans laquelle on est
                self.mat[i][j] = min(s1, s2, s3)
        #Puis on peut alors calculer la distance.
        matrix = np.copy(self.mat)
        res = 0
        def S(A: str, B:str) -> int:
            if A == B:
                return -1
            else:
                return 1
        i = len(self.A) - 1
        j = len(self.B) - 1
        while i > 0 or j > 0:
            pos = (i > 0 and j > 0)
            comp = S(self.A[i], self.B[j])
            if pos and matrix[i][j] == matrix[i - 1][j - 1] + comp:
                # On a pas de trou et il faut comparer les caractères
                self._alignA = f"{self.A[i]}{self._alignA}"
                self._alignB = f"{self.B[j]}{self._alignB}"
                i += -1
                j += -1
                if self.A[i] != self.B[j]:
                    # S'ils sont différents, cela augmente la distance
                    res += egalite
            elif i > 0 and matrix[i][j] == matrix[i - 1][j] + 1:
                # On a un trou à mettre en B
                self._alignA = f"{self.A[i]}{self._alignA}"
                self._alignB = f"={self._alignB}"
                i += -1
                res += (trou - egalite)
                #A chaque fois ces erreurs comptent doubles donc on adapte
            else:
                # On a un trou à mettre en A
                self._alignA = f"={self._alignA}"
                self._alignB = f"{self.B[j]}{self._alignB}"
                j += -1
                res += (trou - egalite)
                #A chaque fois ces erreurs comptent doubles donc on adapte
        self.distance = res

    def report(self) -> tuple:
        """
        Cette fonction vise à donner un compte-rendu de la comparaison
        Par la fonction red_text on met en évidence les différences.
        """
        d = self.distance
        if len(self._alignA) != len(self._alignB):
            raise ValueError("Unexpected Error,distance calculation has failed")
        alignA_print, alignB_print = "", ""
        for k in range(len(self._alignA)):
            # On réécrit en mettant en valeur les changements
            if self._alignA[k] == "=":
                alignA_print += red_text("=")
                alignB_print += self._alignB[k]
            elif self._alignB[k] == "=":
                alignA_print += self._alignA[k]
                alignB_print += red_text("=")
            elif self._alignA[k] != self._alignB[k]:
                alignA_print += red_text(self._alignA[k])
                alignB_print += red_text(self._alignB[k])
            else:
                alignA_print += self._alignA[k]
                alignB_print += self._alignB[k]
        return alignA_print, alignB_print

    @property
    def mat(self):
        """
        Cette property va stocker la matrice de comparaison
        """
        return self._mat