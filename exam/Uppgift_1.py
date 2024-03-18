# uppgift 1:
# ---------- 

# ------------ Uppgift A ------------
import numpy as np

def f(x, y):
    return x**2 + y**2

# Genererar arrays som innehåller heltal inom intervallet
x = np.arange(0, 10)
y = np.arange(0, 8)

# Genererar 2 matriser som representerar X och Y koordinater i ett koordinatsystem
X, Y = np.meshgrid(y, x)

# Skapar en matris som bestäms av resultatet av funktionen f 
# utifrån parametrarna som är x och y koordinaterna från meshgriden
NP_A = f(X, Y)

# ------------ Uppgift B ------------

# Väljer rader 2 & 5 (startindex 2, stoppindex 6(exkluderas), step: 3) och kolumner 1 & 4
subarray = NP_A[2:6:3, [1, 4]] 

print(subarray)

