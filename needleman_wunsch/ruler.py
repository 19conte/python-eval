import numpy as np

class Ruler():

    def __init__(self, brin1 : str, brin2 : str, match_award = 0, mismatch_penalty = 1,
     gap_penalty = 1):
        """ Initialize the 2 sequences"""

        self.brin1 = brin1
        self.brin2 = brin2
        self.AlignmentA = ""
        self.AlignmentB = ""
        self.mismatch_penalty = mismatch_penalty
        self.gap_penalty = gap_penalty
        self.match_award = match_award
        self.distance = 0
        self.n = len(self.brin1)
        self.m = len(self.brin2)

    def _match_score(self, alpha, beta):
        if alpha == beta:
            return self.match_award
        elif alpha == '-' or beta == '-':
            return self.gap_penalty
        else:
            return self.mismatch_penalty

    def _build_F(self):
        """ The entry F[n; m] gives the maximum score among all possible alignments. 
        To compute an alignment that actually gives this score, you start from the bottom right 
        cell, and compare the value with the three possible sources (Match, Insert, and Delete
        above) to see which it came from. [Wikipedia]"""

        F = np.zeros((self.n + 1, self.m + 1))
        for i in range(self.m + 1):
            F[i, 0] = self.gap_penalty*i
        for j in range(self.n + 1):
            F[0, j] = self.gap_penalty*j
        for i in range(1, self.m + 1):
            for j in range(1, self.n + 1):
                Match = F[i-1, j-1] + self._match_score(self.brin1[j - 1], self.brin2[i - 1])
                Delete = F[i-1, j] + self.gap_penalty
                Insert = F[i, j-1] + self.gap_penalty
                F[i, j] = max(Match, Delete, Insert)
        return F
    
    def compute(self):
        F = self._build_F()
        i, j = self.m, self.n 
        # We'll use i and j to keep track of where we are in the matrix
        while i > 0 and j > 0: # end touching the top or the left edge
            score_current = F[i][j]
            score_diagonal = F[i-1][j-1]
            score_up = F[i][j-1]
            score_left = F[i-1][j]
        
        # Check to figure out which cell the current score was calculated from,
        # then update i and j to correspond to that cell.
        if score_current == score_diagonal + self._match_score(self.brin1[j-1], self.brin2[i-1]):
            self.AlignmentA += self.brin1[j-1]
            self.AlignmentB += self.brin2[i-1]
            i -= 1
            j -= 1
        elif score_current == score_up + self.gap_penalty:
            self.AlignmentA += self.brin1[j-1]
            self.AlignmentB += '-'
            j -= 1
        elif score_current == score_left + self.gap_penalty:
            self.AlignmentA += '-'
            self.AlignmentB += self.brin2[i-1]
            i -= 1

        # Finish tracing up to the top left cell
        while j > 0:
            self.AlignmentA += self.brin1[j-1]
            self.AlignmentB += '-'
            j -= 1
        while i > 0:
            self.AlignmentA += '-'
            self.AlignmentB += self.brin2[i-1]
            i -= 1
    
    # Since we traversed the score matrix from the bottom right, our two sequences will be reversed.
    # These two lines reverse the order of the characters in each sequence.
        self.AlignmentA = self.AlignmentA[::-1]
        self.AlignmentB = self.AlignmentB[::-1]       
            

    def report(self):
        return self.AlignmentA, self.AlignmentB
