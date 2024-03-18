# uppgift 2:
# ----------    
import pickle

print("# --------- Uppgift A ---------")
class Dator:
    def __init__(self, tillverkare, modell, ar, pris):
        self.tillverkare = tillverkare
        self.modell = modell
        self.ar = ar
        self.pris = pris

# Lista för att lagra datorobjekt
datorer = []

def lista():
    antal = int(input("Hur många datorer vill du lägga till? "))
    for i in range(antal):
        print(f"Dator {i + 1}:")
        tillverkare = input("Ange tillverkare: ")
        modell = input("Ange modell: ")
        ar = input("Ange tillverkningsår: ")
        pris = input("Ange pris: ")
        dator = Dator(tillverkare, modell, ar, pris)
        datorer.append(dator)

def visa_data():
    print(f"{'Tillverkare':<15} {'Modell':<20} {'År':<5} {'Pris':<10}")
    print("-" * 50)
    for dator in datorer:
        print(f"{dator.tillverkare:<15} {dator.modell:<20} {dator.ar:<5} {dator.pris:<10}")

lista()
visa_data()

print("\n# --------- Uppgift B ---------")
# Detta ersätter den tidigare definitionen av Dator-klassen
class Dator:
    def __init__(self, tillverkare, modell, pris):
        self.tillverkare = tillverkare
        self.modell = modell
        self.pris = pris

class Laptop(Dator):
    def __init__(self, tillverkare, modell, processortyp, ram, pris, skarmstorlek):
        super().__init__(tillverkare, modell, pris)
        self.processortyp = processortyp
        self.ram = ram
        self.skarmstorlek = skarmstorlek

    def visa_information(self):
        print(f"Tillverkare: {self.tillverkare}")
        print(f"Modell: {self.modell}")
        print(f"Processortyp: {self.processortyp}")
        print(f"Installerat RAM: {self.ram} GB")
        print(f"Pris: {self.pris} Kr")
        print(f"Skärmstorlek: {self.skarmstorlek} tum")

min_laptop = Laptop('ASUS', 'ExpertBook', 'Core i5', '16', '7990', '15.6')
min_laptop.visa_information()

print("\n# --------- Uppgift C ---------")
def spara_datorer():
    dator_lista = []
    go_on = 'ja'
    while go_on.lower() == 'ja':
        tillverkare = input("Ange datorns fabrikat: ")
        modell = input("Ange modell: ")
        processortyp = input("Ange processortyp: ")
        ram = input("Ange installerat RAM (GB): ")
        pris = input("Ange pris (kr): ")
        skarmstorlek = input("Ange skärmstorlek (tum): ")
        
        # Skapar en Laptop-instans eftersom den är en underklass med mer specifika attribut
        laptop = Laptop(tillverkare, modell, processortyp, ram, pris, skarmstorlek)
        dator_lista.append(laptop)
        
        go_on = input("Vill du ange flera datorer? (ja/nej): ")
    
    # Serialisering och sparande av dator_lista till filen dator.dat
    # "wb" == write binary
    with open("dator.dat", "wb") as dator_fil:
        pickle.dump(dator_lista, dator_fil)
    
    print("Data är skriven i filen dator.dat.")

spara_datorer()

print("\n# --------- Uppgift D ---------")
def ladda_data():
    # Använd pickle.load för att avserialisera datan
    try:
        with open("dator.dat", "rb") as dator_fil:
            return pickle.load(dator_fil)
    except FileNotFoundError:
        print("Filen dator.dat hittades inte.")
        return []

def visa_data(datorer):
    for dator in datorer:
        print(f"Tillverkare: {dator.tillverkare}")
        print(f"Modell: {dator.modell}")
        if isinstance(dator, Laptop):  # Felkontroll
            print(f"Processortyp: {dator.processortyp}")
            print(f"Installerad RAM: {dator.ram} GB")
            print(f"Pris: {dator.pris} Kr")
            print(f"Skärmstorlek: {dator.skarmstorlek} tum")
        print() 

loaded_datorer = ladda_data()
visa_data(loaded_datorer)