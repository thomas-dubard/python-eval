from collections import namedtuple

class Codec:
    """
    Cette classe vise à utiliser les arbres de la classe TreeBuilder.
    On va donc récupérer l'arbre correspondant dans tree.
    On va ensuite encoder et décoder le texte grâce à la clé donnée par tree.
    """
    def __init__(self, tree):
        self.tree = tree
        self.dico = None
        self.rev_dico = None

    def encode(self, text):
        """
        On fusionne les codages de toutes les lettres du texte.
        On prendra ce long chiffre en chaîne de caractères.
        de plus cela simplifie la concaténation des codes.
        """
        return "".join(self.dico[x] for x in text)

    def decode(self, encoded):
        """
        On profite du dictionnaire de décodage rev_dico.
        On stocke ce que l'on voit au fur et à mesure.
        Dès que l'on détecte une séquence connue, on décode et on continue.
        Normalement le tri dans tree.HDD permet de ne pas avoir d'erreurs.
        Autrement on peut avoir des recouvrements, comme l'exemple ci-dessous:
        b = 00 et c=000 pose un problème lors du décodage...
        """
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
        """
        On va définir le dictionnaire de self comme property.
        On va s'appuyer sur la structure de self.tree.
        Grâce au namedTuple il suffit de regarder si l'élément est un tuple,
        sachant qu'au bout des branches il y a des listes à deux éléments.
        Si on est sur un namedTuple, c'est que l'on peut s'enfoncer.
        """
        current = [[self.tree, ""]]
        check = sum(isinstance(x[0], tuple) for x in current)
        while check > 0:
            # On continue tant qu'on a pas fini toutes les branches de tree
            swap = []
            for x in current:
                if isinstance(x[0], tuple):
                    swap.extend([[x[0][0], f"0{x[1]}"], [x[0][1], f"1{x[1]}"]])
                elif isinstance(x[0], list):
                    swap.append(x)
            current = swap[:]
            check = sum(isinstance(x[0], tuple) for x in current)

        # La suite vise à éjecter toutes les erreurs de type de l'arbre.
        # Théoriquement il n'y en a pas, mais c'est une sécurité.
        error = []
        for k in range(len(current)):
            if not isinstance(current[k], list):
                error.append(k)
        for k in error[::-1]:
            current.pop(k)

        result = dict()
        for x in current:
            result[x[0][0]] = x[1]
            # A chaque caractère on associe son codage binaire.

        # La suite vise à éjecter les None ou chaînes vides produites par tree.
        if None in result:
            result.pop(None)
        if "" in result:
            result.pop("")

        # Comme il y a des recouvrements ...
        # On va devoir les corriger manuellement ...
        for k in range(len(self.tree.HDD)):
            xk = self.tree.HDD[k][0]
            nk = len(result[xk])
            for i in range(len(self.tree.HDD)):
                xi = self.tree.HDD[i][0]
                ni = len(result[xi])
                if i!= k and nk <= ni and xk == xi[:nk]:
                    # Alors il y a recouvrement.
                    # D'expérience ils ne sont qu'à une lettre près ...
                    # On va espérer que c'est toujours le cas ...
                    if xi[nk] == "0":
                        xk += "1"
                    else:
                        xk += "0"

        # Au cas où on vérifie que ça a été efficace ...
        for k in range(len(self.tree.HDD)):
            xk = self.tree.HDD[k][0]
            nk = len(result[xk])
            for i in range(len(self.tree.HDD)):
                xi = self.tree.HDD[i][0]
                ni = len(result[xi])
                if i!= k and nk <= ni and xk == xi[:nk]:
                    raise ValueError("Echec critique: il reste des erreurs !")

        self._dico = result

    @rev_dico.setter
    def rev_dico(self, dico):
        """
        Pour faciliter le décodage on renverse le dictionnaire de codage.
        C'est légitime car ce dictionnaire self.dico est bijectif.
        """
        dico_swap = dict()
        for x in self.dico:
            dico_swap[self.dico[x]] = x
        self._rev_dico = dico_swap


class TreeBuilder:
    """
    Cette classe vise à construire l'arbre pour le codage.
    Pour cela on va s'appuyer sur la fonction tree qui va la construire.
    Dans text on stocke le texte donné en entrée.
    Dans stock on met l'ensemble des caractères à coder.
    Dans occure on associe aux caractères leur nombre d'occurences dans text
    Dans HDD on va stocker ces caractères avec ce nombre,
    mais par ordre décroissant de nombre d'occurences.
    """
    def __init__(self, text):
        """
        NB: les arbres sont schizophrènes...
        En interne dans le init 'Smeagol' a des variables comme HDD.
        Mais une fois instancé, on a plus que 'Gollum' le BinaryNode.
        Or on aimerait bien avoir les deux ...
        Je vais probablement devoir adapter les arguments de Codec ...
        """
        self.text = text
        self.stock = set(self.text) #on identifie les caractères à coder
        occur = dict()
        for x in self.stock:
            occur[x] = sum((x == y) for y in self.text)
        self.occur = occur #on regarde le nombre d'occurences des caractères

        self.HDD = [] #liste pour ordonner les caractères par ordre d'importance
        for x in self.stock:
            self.HDD.append((x, self.occur[x]))
        i = 0 #On va faire un tri par sélection
        while i < len(self.stock):
            maxi = (None, 0)
            k = i
            record = i
            while k < len(self.stock):
                if self.HDD[k][1] > maxi[1]:
                    maxi = self.HDD[k]
                    record = k
                k += 1
            self.HDD[i], self.HDD[record] = self.HDD[record], self.HDD[i]
            i += 1
        print(f"HDD={self.HDD}")


    def tree(self):
        """
        A partir de la fonction Binary on récupère les noeuds binaires.
        On va ensuite constituer un arbre avec ces noeuds.
        """
        BinaryNode = namedtuple('BinaryNode', ['g0', 'd1', 'id'])
        def Binary(text, nb, id):
            """
            On va constituer l'arbre binaire par récursivité.
            Au-dessus on a défini le namedtuple BinaryNode.
            Il permet d'écrire plus proprement les parcours dans l'arbre.
            Il suffit de donner les instructions et de les composer.
            Alors g0 définit un aller à gauche.
            Et d1 un aller à droite.
            De plus on affecte à chaque noeud un identifiant id.
            cela va permettre d'aisément faire le codage en binaire.
            En dehors des cas de base, on va chercher à couper le texte en deux.
            Pour optimiser la découpe, on l'aura trié au préalable via HDD.
            """
            # Cas de base
            if len(text) == 1: #juste un caractère et son nombre d'occurences
                return [text, nb, id]
            if len(text) == 0: #rien mais on le met quand même
                return ["", 0, None]
            if len(text) == 2: #pour s'assurer du bon fonctionnement
                # et montre la philosophie du codage de l'arbre ici
                # et évite des erreurs sur les partages médians à deux éléments
                text1 = text[0]
                nb1 = self.occur[text1]
                text2 = text[1]
                nb2 = self.occur[text2]
                return BinaryNode(Binary(text1, nb1), Binary(text2, nb2))

            # Cas général
            queue = []
            k, cpt = 0, 0
            while k < len(text) and cpt < nb//2:
                # On essaie de faire une coupe médiane sur l'occurence.
                queue.append(text[k])
                cpt += self.occur[text[k]]
                k += 1
            n = len(queue)
            text1 = "".join(x for x in queue)
            nb1 = sum(self.occur[x] for x in text1)
            text2 = "".join(x for x in text[n:])
            nb2 = sum(self.occur[x] for x in text2)
            return BinaryNode(Binary(text1, nb1), Binary(text2, nb2))

        texte = "".join(x[0] for x in self.HDD)
        nombre = sum(self.occur[x] for x in self.stock)
        print(f"texte = {texte}, nombre = {nombre}")
        return Binary(texte, nombre)