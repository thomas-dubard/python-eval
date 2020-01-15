from collections import namedtuple

class Codec:
    def __init__(self, tree):
        pass

    def encode(self, text):
        pass

    def decode(self, text):
        pass

class TreeBuilder:
    def __init__(self, text):
        self.text = text
        self.stock = set(self.text)
        occur = dict()
        for x in stock:
            occur[x] = sum((x == y) for y in self.text)
        self.occur = occur

    def tree(self):
        BinaryNode = namedtuple('BinaryNode', ['g0', 'd1'])
        def Binary(text, nb):   #récursif
            if len(text) == 1:
                return text, nb
            if len(text) == 0:
                return None
            queue = []
            k, cpt = 0, 0
            while k < len(text) and cpt < len(text)//2:
                queue.append(text[k])
                cpt += self.occur[k]
                k += 1
            n = len(queue)
            text1 = "".join(x for x in queue)
            nb1 = sum(self.occur[x] for x in text1)
            text2 = "".join(x for x in text[n:])
            nb2 = sum(self.occur[x] for x in text2)
            return BinaryNode(Binary(text1, nb1), Binary(text2, nb2))