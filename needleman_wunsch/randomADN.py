import string
import random

N = 1000

# Affiche deux chaînes de caractères composées de A, T, G, C, de longueur N

sequence1 = ''.join(random.choices("ATGC", k = N)) 
sequence2 = ''.join(random.choices("ATGC", k = N)) 

print(sequence1)
print(sequence2)