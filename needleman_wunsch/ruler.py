import numpy as np

class Ruler():

    def __init__(self, brin1 : str, brin2 : str, d : int = 1):
        """ Initialize the 2 sequences"""

        self.brin1 = brin1
        self.brin2 = brin2
        self.AlignmentA = ""
        self.AlignmentB = ""
        self.d = d
        self.distance = 0
        self.n = len(self.brin1)
        self.m = len(self.brin2)
    
    def _substitution(self, i : int, j : int):
        """ Switching 2 different letters 'costs' 1"""
        
        if self.brin1[i] == self.brin2[j]:
            return 0
        else:
            return 1

    def _build_F(self):
        """ The entry F[n; m] gives the maximum score among all possible alignments. 
        To compute an alignment that actually gives this score, you start from the bottom right 
        cell, and compare the value with the three possible sources (Match, Insert, and Delete
        above) to see which it came from. [Wikipedia]"""

        F = np.zeros((self.n + 1, self.m + 1))
        for i in range(self.n):
            F[i, 0] = self.d*i
        for j in range(self.m):
            F[0, j] = self.d*j
        for i in range(1, self.n + 1):
            for j in range(1, self.m + 1):
                Match = F[i-1, j-1] + self._substitution(i - 1, j - 1)
                Delete = F[i-1, j] + self.d
                Insert = F[i, j-1] + self.d
                F[i, j] = max(Match, Delete, Insert)
        return F
    
    def compute(self):
        F = self._build_F()
        i, j = self.n - 1, self.m - 1
        while i > 0 or j > 0:
            if i > 0 and j > 0 and F[i, j] == F[i -1, j - 1] + self._substitution(i, j):
                self.AlignmentA += self.brin1[i]
                self.AlignmentB += self.brin2[j]
                i -= 1
                j -= 1
            elif i > 0 and F[i, j] == F[i - 1, j] + self.d:
                self.AlignmentA += self.brin1[i]
                self.AlignmentB += "-"
                i -= 1
            else:
                self.AlignmentA += "-"
                self.AlignmentB += self.brin2[j]
                j -= 1
        for (a, b) in zip (self.brin1, self.brin2):
            if a == "-" or b == "-":
                self.distance += 1
            elif a != b:
                self.distance += 1
            

    def report(self):
        return self.AlignmentA, self.AlignmentB
