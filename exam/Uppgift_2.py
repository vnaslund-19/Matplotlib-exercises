# uppgift 2:
# ----------    
import pickle

def is_numeric(value):
    return value.replace('.', '', 1).isdigit()

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
    while True:
        try:
            antal = int(input("Hur många datorer vill du lägga till? "))
            break 
        except ValueError:
            print("Felaktig inmatning. Ange ett heltal.")
    for i in range(antal):
        print(f"Dator {i + 1}:")
        tillverkare = input("Ange tillverkare: ")
        modell = input("Ange modell: ")
        while True:
            try:
                ar = int(input("Ange tillverkningsår: "))
                break 
            except ValueError:
                print("Felaktig inmatning. Ange ett heltal.")
        while True:
            pris = input("Ange pris: ")
            if is_numeric(pris):
                pris = float(pris)
                break
            else:
                print("Felaktig inmatning. Ange ett numeriskt värde för pris.")
        dator = Dator(tillverkare, modell, ar, pris)
        datorer.append(dator)

def visa_data():
    print(f"{'Tillverkare':<20} {'Modell':<20} {'År':<10} {'Pris':<10}")
    print("-" * 50)
    for dator in datorer:
        print(f"{dator.tillverkare:<20} {dator.modell:<20} {dator.ar:<10} {dator.pris:<10}")

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
        while True:
            ram = input("Ange installerat RAM (GB): ")
            if is_numeric(ram):
                pris = float(ram)
                break
            else:
                print("Felaktig inmatning. Ange ett numeriskt värde för RAM.")
        while True:
            pris = input("Ange pris: ")
            if is_numeric(pris):
                pris = float(pris)
                break
            else:
                print("Felaktig inmatning. Ange ett numeriskt värde för pris.")
        while True:
            skarmstorlek = input("Ange skärmstorlek (tum): ")
            if is_numeric(skarmstorlek):
                skarmstorlek = float(skarmstorlek)
                break
            else:
                print("Felaktig inmatning. Ange ett numeriskt värde för skärmstorlek.")
        
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