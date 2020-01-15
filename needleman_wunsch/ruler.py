import numpy as np

class Ruler:
    def __init__(self, str1, str2):
        self.distance = None
        self._alignA = ""
        self._alignB = ""

    def compute(self):

        #construction de la matrice
        swap = [0 for _ in range(len(str2 + 1))]
        mat = np.array([swap for _ in range(len(str1 + 1))])

       #remplissage de la matrice
        mat[0][:] = [k for k in range(len(str2 + 1))]
        mat[:][0] = [k for k in range(len(str1 + 1))]
        for i in range(1, len(str1 + 1)):
            for j in range(1, len(str2 + 1)):
                if str1[j] == str2[i]:
                    s1 = mat[i - 1][j - 1] - 1
                else:
                    s1 = mat[i - 1][j - 1] + 1
                s2 = mat[i][j - 1] + 1
                s3 = mat[i - 1][j] + 1
                mat[i][j] = min(s1, s2, s3)

    def report(self):
        return self._alignA, self._alignB

    @property
    def distance(self):
        return self._distance

    @distance.setter
    def distance():
        res = 0
        def S(A, B):
            if A == B:
                return -1
            else:
                return 1
        A = str1
        B = str2
        i = len(str1)
        j = len(str2)
        while i > 0 or j > 0:
            pos = (i > 0 and j > 0)
            if pos and mat[i][j] == mat[i - 1][j - 1] + S(A[i], B[j]):
                "".join(A[i], self._alignA)
                "".join(B[j], self._alignB)
                i += -1
                j += -1
                if A[i] != B[j]:
                    res += 1
            elif i > 0 and mat[i][j] == mat[i - 1][j] + 1:
                "".join(A[i], self._alignA)
                "".join("-", self._alignB)
                i += -1
                res += 1
            else:
                "".join("-", self._alignA)
                "".join(B[j], self._alignB)
                j += -1
                res += 1
        self._distance = res