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


print("# --------- Uppgift B ---------")
# Väljer rader 2 & 5 (startindex 2, stoppindex 6(exkluderas), step: 3) och kolumner 1 & 4
extract = NP_A[2:6:3, [1, 4]] 

print(extract)

print("\n# --------- Uppgift C ---------")
# Skapar en ny array med alla element från NP_A fast i en endimensionell array
flattened_list = NP_A.flatten() 

filtered_elements = flattened_list[(flattened_list > 20) & (flattened_list < 50)]

print("Endimensionell lista:")
print(flattened_list)
print("\nUtvalda element:")
print(filtered_elements)

print("\n# --------- Uppgift D ---------")
# Räkna ut summan av min och max värdet i varje rad
min_plus_max_sum_array = NP_A.max(axis=1) + NP_A.min(axis=1)

print("Summor:")
for i in range (10):
    print(f"Rad {i}: {min_plus_max_sum_array[i]}")

print("\n# --------- Uppgift E ---------")
max_107_NP_A = np.where(NP_A > 107, -100, NP_A)

print(max_107_NP_A)

print("\n# --------- Uppgift F ---------")

# Skapa en lista där alla kvadrater av 0-9 repeteras 5 gånger
base_numbers = np.arange(10)
squared_repeated = np.repeat(base_numbers**2, 5)

NP_Arr = np.where(squared_repeated % 10 == 9, 112, squared_repeated)

print(NP_Arr)