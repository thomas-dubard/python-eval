import numpy as np
from colorama import Fore, Style

def red_text(text):
    return f"{Fore.RED}{text}{Style.RESET_ALL}"

class Ruler:
    def __init__(self, str1, str2):
        self._alignA = ""
        self._alignB = ""
        self.A = str1
        self.B = str2
        self.distance = 0
        #construction de la matrice
        nb_col = len(self.B)
        nb_ligne = len(self.A)
        self.mat = np.array([[0]*(nb_col+1)]*(nb_ligne+1))

    def compute(self):
       #remplissage de la matrice
        self.mat[0][:] = range(nb_col + 1)
        self.mat.T[0][:] = [k for k in range(nb_ligne + 1)]
        self.mat.T
        for i in range(1, nb_ligne):
            for j in range(1, nb_col):
                if self.A[i] == self.B[j]:
                    s1 = self.mat[i - 1][j - 1] - 1
                else:
                    s1 = self.mat[i - 1][j - 1] + 1
                s2 = self.mat[i][j - 1] + 1
                s3 = self.mat[i - 1][j] + 1
                self.mat[i][j] = min(s1, s2, s3)
        print("ok")

    def report(self):
        d = self.distance
        if len(self._alignA) != len(self._alignB):
            raise ValueError("Unexpected Error,distance calculation has failed")
        alignA_print, alignB_print = "", ""
        for k in range(len(self._alignA)):
            if alignA[k] == "=":
                "".join(alignA_print, red_text("="))
                "".join(alignB_print, alignB[k])
            elif alignB[k] == "=":
                "".join(alignA_print, alignA[k])
                "".join(alignB_print, red_text("="))
            elif alignA[k] != alignB[k]:
                "".join(alignA_print, red_text(alignA[k]))
                "".join(alignB_print, red_text(alignB[k]))
            else:
                "".join(alignA_print, alignA[k])
                "".join(alignB_print, alignB[k])
        return alignA_print, alignB_print

    @property
    def distance(self):
        return self._distance

    @distance.setter
    def distance(self, matrix):
        res = 0
        def S(A, B):
            if A == B:
                return -1
            else:
                return 1
        i = len(self.A)
        j = len(self.B)
        while i > 0 or j > 0:
            pos = (i > 0 and j > 0)
            if pos and self.mat[i][j] == self.mat[i - 1][j - 1] + S(self.A[i], self.B[j]):
                "".join(self.A[i], self._alignA)
                "".join(self.B[j], self._alignB)
                i += -1
                j += -1
                if self.A[i] != self.B[j]:
                    res += 1
            elif i > 0 and self.mat[i][j] == self.mat[i - 1][j] + 1:
                "".join(self.A[i], self._alignA)
                "".join("=", self._alignB)
                i += -1
                res += 1
            else:
                "".join("=", self._alignA)
                "".join(self.B[j], self._alignB)
                j += -1
                res += 1
        self._distance = res