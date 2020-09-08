class Bor:

    def __init__(self, parent=None, symbol=-1):
        self.is_word = False
        self.parent = parent
        self.next = [-1 for x in range(33)]
        self._symbol = symbol
        self._suf_link = -1
        self._good_suf_link = -1
        self._auto_move = [-1 for x in range(33)]

    def add_word(self, word):
        """add a word in the bor"""

        leaf = self
        for c in word:
            id_l = ord(c) - ord('а')

            if leaf.next[id_l] == -1:
                leaf.next[id_l] = Bor(leaf, id_l)

            leaf = leaf.next[id_l]

        leaf.is_word = True

    def check_for_equality(self, word):
        """check whether the word is bor substrings"""

        leaf = self
        for c in word:
            id_l = ord(c) - ord('а')

            if id_l >= 33 or id_l < 0:
                continue

            leaf = leaf.next[id_l]

            if leaf == -1:
                return False

        return leaf.is_word

    def get_suf_link(self):
        """return a suffix link for the vertex"""

        if self._suf_link == -1:
            if self.parent is None:
                self._suf_link = self
            elif self.parent.parent is None:
                self._suf_link = self.parent
            else:
                self._suf_link = self.parent.get_suf_link().get_auto_move(self._symbol)

        return self._suf_link

    def get_auto_move(self, ch):
        """return a vertex for move from one state to another by character"""

        if self._auto_move[ch] == -1:
            if self.next[ch] != -1:
                self._auto_move[ch] = self.next[ch]
            elif self.parent is None:
                self._auto_move[ch] = self
            else:
                self._auto_move[ch] = self.get_suf_link().get_auto_move(ch)

        return self._auto_move[ch]

    def get_good_suf_link(self):
        """return a 'good' suffix link for the vertex"""

        if self._good_suf_link == -1:
            sl = self.get_suf_link()

            if sl.parent is None or sl.is_word:
                self._good_suf_link = sl
            else:
                self._good_suf_link = sl.get_good_suf_link()

        return self._good_suf_link

    def check_word(self, word):
        """check whether the word is bor substrings"""

        leaf = self
        for c in word:
            id_l = ord(c) - ord('а')

            if id_l >= 33 or id_l < 0:
                continue

            leaf = leaf.get_auto_move(id_l)

            if leaf.get_good_suf_link() is not None and leaf.is_word:
                return True

        return False
