#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

class Ruler():
    """ Crée une instance de calcul de distance """

    def __init__(self, brin1 : str, brin2 : str, match_award = 0, mismatch_penalty = 1,
     gap_penalty = 1):
        """ Initialise les deux chaînes de caractères à comparer. L'utilisateur peut préciser 
        le coût d'un échange de lettre et le coût d'une insertion/suppression """

        self.brin1 = brin1
        self.brin2 = brin2
        #on stocke la longueur des 2 chaînes à comparer
        self.n = len(self.brin1) 
        self.m = len(self.brin2)
        # On initialise les alignements optimaux des deux chaînes, que l'on va construire après.
        self.AlignmentA = ""
        self.AlignmentB = ""
        self.mismatch_penalty = mismatch_penalty
        self.gap_penalty = gap_penalty
        self.match_award = match_award
        self.distance = 0 

    def _match_score(self, a, b):
        """ Compare deux caractères et renvoie le score correspondant """

        if a == b:
            return self.match_award
        elif a == '=' or b == '=':
            return self.gap_penalty
        else:
            return self.mismatch_penalty

    def _build_F(self):
        """ The entry F[n; m] gives the maximum score among all possible alignments. 
        To compute an alignment that actually gives this score, you start from the bottom right 
        cell, and compare the value with the three possible sources (Match, Insert, and Delete
        above) to see which it came from. [Wikipedia]"""

        F = np.zeros((self.m + 1, self.n + 1))
        for i in range(self.m + 1):
            F[i, 0] = self.gap_penalty*i
        for j in range(self.n + 1):
            F[0, j] = self.gap_penalty*j
        for i in range(1, self.m + 1):
            for j in range(1, self.n + 1):
                Match = F[i-1, j-1] + self._match_score(self.brin1[j - 1], self.brin2[i - 1])
                Delete = F[i-1, j] + self.gap_penalty
                Insert = F[i, j-1] + self.gap_penalty
                F[i, j] = min(Match, Delete, Insert)
        return F
    
    def compute(self):
        """ On lit la matrice F de en bas à droite à en haut à gauche. On remonte de case en 
        case en déterminant comment on a obtenu le score de la case traitée, lors de 
        la construction de la matrice F. On construit progressivement AignmentA et AlignmentB. """

        F = self._build_F()
        i, j = self.m, self.n # On se place en bas à droite dans la matrice F.
       
        while i > 0 and j > 0:
            score_current = F[i][j]
            score_diagonal = F[i-1][j-1]
            score_up = F[i][j-1]
            score_left = F[i-1][j]

            # Si on vient la case en diagonal au-dessus:
            if score_current == score_diagonal + self._match_score(self.brin1[j-1],
             self.brin2[i-1]):
                self.AlignmentA += self.brin1[j-1]
                self.AlignmentB += self.brin2[i-1]
                i -= 1
                j -= 1
            # Si on vient de la case au-dessus:
            elif score_current == score_up + self.gap_penalty:
                self.AlignmentA += self.brin1[j-1]
                self.AlignmentB += '='
                j -= 1
            # Si on vient de la case à gauche:
            elif score_current == score_left + self.gap_penalty:
                self.AlignmentA += '='
                self.AlignmentB += self.brin2[i-1]
                i -= 1
            # On a atteint la première ligne de la matrice F:
        while j > 0:
            self.AlignmentA += self.brin1[j-1]
            self.AlignmentB += '='
            j -= 1
        # On a atteint la première colonne de la matrice F:
        while i > 0:
            self.AlignmentA += '='
            self.AlignmentB += self.brin2[i-1]
            i -= 1
    
    # On a parcouru la matrice F de en bas à droite à en haut à gauche,
    # donc il faut retourner les chaines de caractères renvoyées par compute
        self.AlignmentA = self.AlignmentA[::-1]
        self.AlignmentB = self.AlignmentB[::-1]    

        # Calcul de la distance par parcours simultané des 2 chaînes
        for a, b in zip(self.AlignmentA, self.AlignmentB):
            self.distance += self._match_score(a, b)
            

    def report(self):
        """ Retourne les chaînes de caractères modifiées. Les tirets signifient qu'il y a eu 
        une insertion ou suppression """

        return self.AlignmentA, self.AlignmentB
