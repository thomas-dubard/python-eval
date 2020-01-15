from collections import namedtuple

class Codec:
    def __init__(self, tree):
        self.tree = tree
        self.dico = None
        self.rev_dico = None

    def encode(self, text):
        return "".join(self.dico[x] for x in text)

    def decode(self, encoded):
        queue = ""
        res = []
        print(self.dico)
        print(self.rev_dico)
        for x in encoded:
            if queue in self.rev_dico:
                res.append(self.rev_dico[queue])
                print(queue)
                queue = x
            else:
                queue = queue + x
        print(queue)
        res.append(self.rev_dico[queue])
        return "".join(x for x in res)

    @property
    def dico(self):
        return self._dico

    @property
    def rev_dico(self):
        return self._rev_dico

    @dico.setter
    def dico(self, tree):
        current = [[self.tree, ""]]
        check = sum(isinstance(x[0], tuple) for x in current)
        while check > 0:
            swap = []
            for x in current:
                if isinstance(x[0], tuple):
                    swap.extend([[x[0][0], f"0{x[1]}"], [x[0][1], f"1{x[1]}"]])
                elif isinstance(x[0], list):
                    swap.append(x)
            current = swap[:]
            check = sum(isinstance(x[0], tuple) for x in current)
        error = []
        for k in range(len(current)):
            if not isinstance(current[k], list):
                error.append(k)
        for k in error[::-1]:
            current.pop(k)
        result = dict()
        for x in current:
            result[x[0][0]] = x[1]
        if None in result:
            result.pop(None)
        if "" in result:
            result.pop("")
        self._dico = result

    @rev_dico.setter
    def rev_dico(self, dico):
        dico_swap = dict()
        for x in self.dico:
            dico_swap[self.dico[x]] = x
        self._rev_dico = dico_swap


class TreeBuilder:
    def __init__(self, text):
        self.text = text
        self.stock = set(self.text)     #a trier
        occur = dict()
        for x in self.stock:
            occur[x] = sum((x == y) for y in self.text)
        self.occur = occur


    def tree(self):
        BinaryNode = namedtuple('BinaryNode', ['g0', 'd1'])
        def Binary(text, nb):   #récursif
            if len(text) == 1:
                return [text, nb]
            if len(text) == 0:
                return ["", 0]
            if len(text) == 2:
                text1 = text[0]
                nb1 = self.occur[text1]
                text2 = text[1]
                nb2 = self.occur[text2]
                return BinaryNode(Binary(text1, nb1), Binary(text2, nb2))
            queue = []
            k, cpt = 0, 0
            while k < len(text) and cpt < nb//2:
                queue.append(text[k])
                cpt += self.occur[text[k]]
                k += 1
            n = len(queue)
            text1 = "".join(x for x in queue)
            nb1 = sum(self.occur[x] for x in text1)
            text2 = "".join(x for x in text[n:])
            nb2 = sum(self.occur[x] for x in text2)
            return BinaryNode(Binary(text1, nb1), Binary(text2, nb2))
        texte = "".join(self.stock)
        nombre = sum(self.occur[x] for x in self.stock)
        return Binary(texte, nombre)