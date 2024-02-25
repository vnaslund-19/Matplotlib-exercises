import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 1
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:
df_cia_factbook = pd.read_csv('cia_factbook.csv', delimiter=';')
df_worldcities = pd.read_csv('worldcities.csv', delimiter=';')
df_worldpubind = pd.read_csv('worldpubind.csv', delimiter=';')

# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 2
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:
df_cia_factbook['density'] = df_cia_factbook['population'] / df_cia_factbook['area'] # skapar en ny kolumn density

# Ta bort rader där 'density' är inf eller NaN
df_cia_factbook.replace([np.inf, -np.inf], np.nan, inplace=True)  # Ersätt inf/-inf med NaN
df_cia_factbook.dropna(subset=['density'], inplace=True)  # Ta bort rader med NaN i 'density'

def plot_density(df, input_value):
    try:
        # Kontrollerar om inmatningen är ett landsnamn
        if df['country'].str.contains(input_value, case=False, regex=False).any():
            country_density = df.loc[df['country'].str.lower() == input_value.lower(), 'density'].iloc[0]
            print(f"Befolkningstäthet för {input_value}: {country_density} invånare/km²")
        else:
            # Kontrollerar och hanterar inmatning för att säkerställa att högst 10 länder visas
            if '+' in input_value or '-' in input_value:
                num_countries = min(int(input_value.rstrip('+-')), 10)  # Begränsar till högst 10 länder
            else:
                num_countries = min(int(input_value), 10)  # Direkt begränsning om användaren matar in ett nummer
            
            ascending = '-' in input_value
            selected_countries = df.sort_values(by='density', ascending=ascending).head(num_countries)

            # Plottar resultatet
            plt.figure(figsize=(10, 8))
            plt.bar(selected_countries['country'], selected_countries['density'], color='skyblue')
            plt.xlabel('Länder')
            plt.ylabel('Befolkningstäthet (invånare/km²)')
            plt.xticks(rotation=45, ha="right")
            plt.title('Befolkningstäthet per Land')
            plt.tight_layout()
            plt.show()
    except Exception:
        print("Felaktig inmatning. Ange ett giltigt antal länder (ex: 3+, 4-) eller ett specifikt landsnamn.")

"""
input_value = input("Ange antal länder (med + för högst och - för lägst) eller ett landsnamn: ")
plot_density(df_cia_factbook, input_value)
"""

# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 3
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:
def menu_option_1(df):
    mean_population = df['population'].mean()
    mean_area = df['area'].mean()
    
    filtered_countries = df[(df['population'] > mean_population) &
                            (df['area'] < mean_area) &
                            (df['birth_rate'].between(15, 24)) &
                            (df['life_exp_at_birth'] > 70)]
    
    print(filtered_countries[['country', 'area', 'birth_rate', 'life_exp_at_birth']].to_string(index=False))

def menu_option_2(df):
    df['Internet Users per 100K'] = (df['internet_users'] / df['population']) * 100000
    
    # Ta bort rader med NaN i 'Internet Users per 100K'
    df_filtered = df.dropna(subset=['Internet Users per 100K'])
    
    # Sortera och välj ut de 5 länderna med lägst och högst internetanvändartäthet
    sorted_df = df_filtered.sort_values('Internet Users per 100K')
    lowest_density_countries = sorted_df.head(5)
    highest_density_countries = sorted_df.tail(5)
    
    # Skriv ut de valda länderna och deras internetanvändartäthet
    print("Countries with the lowest number of internet users per 100,000 inhabitants:")
    print(lowest_density_countries[['country', 'population', 'Internet Users per 100K']].to_string(index=False))
    print("\nCountries with the highest number of internet users per 100,000 inhabitants:")
    print(highest_density_countries[['country', 'population', 'Internet Users per 100K']].to_string(index=False))

def menu_option_3(df):
    df['population_growth_rate'] = (df['birth_rate'] - df['death_rate'] + df['net_migration_rate'])
    df['population_change'] = df['population_growth_rate']  # Antagligen redan i procent per 1000 invånare
    
    # Rensa bort rader med NaN i de nya kolumnerna
    df.dropna(subset=['population_growth_rate', 'population_change'], inplace=True)

    # Sortera df i fallande ordning baserat på 'population_change' för att få de mest negativa förändringarna först
    sorted_df_desc = df.sort_values('population_change', ascending=True)
    # Ta de fem första som är de med mest negativ förändring
    most_negative_change = sorted_df_desc.head(5)
    
    # Sortera df i stigande ordning för att få de mest positiva förändringarna sist
    sorted_df_asc = df.sort_values('population_change', ascending=False)
    # Ta de fem första som är de med mest positiv förändring
    most_positive_change = sorted_df_asc.head(5)
    
    # Konkatenera de två grupperna
    filtered_countries = pd.concat([most_negative_change, most_positive_change])
    
    # Skriv ut de valda länderna och deras förändringsdata
    print(filtered_countries[['country', 'birth_rate', 'death_rate', 'net_migration_rate', 'population_change']].to_string(index=False))
    
    # Skapa ett stapeldiagram för de valda länderna
    plt.figure(figsize=(10, 8))
    # Observera att vi använder 'filtered_countries' direkt eftersom de redan är i rätt ordning
    plt.bar(filtered_countries['country'], filtered_countries['population_change'], color='skyblue')
    plt.xlabel('Länder')
    plt.ylabel('Befolkningsförändring per 1000 invånare')
    plt.xticks(rotation=45, ha="right")
    plt.title('Befolkningsförändring per Land')
    plt.tight_layout()
    plt.show()


def menu():
    while True:
        print("\nUPPGIFT 3 MENY\nVälj ett alternativ:")
        print("1: Visa länder enligt specifika kriterier")
        print("2: Visa länder baserat på internetanvändare per 100.000 invånare")
        print("3: Visa länder med mest positiv och negativ befolkningsförändring")
        print("4: Gå ut ur menyn")
    
        choice = input("Ange ditt val: ")
    
        if choice == '1':
            menu_option_1(df_cia_factbook)
        elif choice == '2':
            menu_option_2(df_cia_factbook)
        elif choice == '3':
            menu_option_3(df_cia_factbook)
        elif choice == '4':
            print("Avslutar programmet...")
            break
        else:
            print("Ogiltigt val, försök igen.")


# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 4
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:
def calculate_population_change(df, year_start, year_end):
    df['population_change_percent'] = ((df[year_end] - df[year_start]) / df[year_start]) * 100
    return df

# Funktion för att skriva ut och plotta de länder med störst och minst procentuell förändring
def plot_population_change(df):
    largest_decrease = df.nsmallest(5, 'population_change_percent')
    largest_increase = df.nlargest(5, 'population_change_percent')
    
    # Tabell
    print("De 5 länderna med störst befolkningsminskning:")
    print(largest_decrease[['Country Name', 'population_change_percent']].to_string(index=False))
    print("\nDe 5 länderna med störst befolkningsökning:")
    print(largest_increase[['Country Name', 'population_change_percent']].to_string(index=False))
    
    # Stapeldiagram för minskning
    plt.figure(figsize=(10, 8))
    plt.bar(largest_decrease['Country Name'], largest_decrease['population_change_percent'], color='red')
    plt.xlabel('Länder')
    plt.ylabel('Procentuell befolkningsförändring')
    plt.title('Länder med störst befolkningsminskning 1960-2021')
    plt.tight_layout()
    plt.show()
    
    # Stapeldiagram för ökning
    plt.figure(figsize=(10, 8))
    plt.bar(largest_increase['Country Name'], largest_increase['population_change_percent'], color='green')
    plt.xlabel('Länder')
    plt.ylabel('Procentuell befolkningsförändring')
    plt.title('Länder med störst befolkningsökning 1960-2021')
    plt.tight_layout()
    plt.show()

# Uppgift b
def annual_population_change_chart(df, country_name):
    country_data = df[df['Country Name'].str.lower() == country_name.lower()].iloc[0]
    years = [str(year) for year in range(1961, 2022)]
    annual_changes = [(country_data[year] - country_data[str(int(year)-1)]) / country_data[str(int(year)-1)] * 100 for year in years]
    
    # Linjediagram över årlig procentuell förändring
    plt.figure(figsize=(15, 8))
    plt.plot(years, annual_changes, marker='o', label='Årlig förändring', color='blue')
    plt.xlabel('År')
    plt.ylabel('Procentuell förändring', color='blue')
    plt.title(f'Årlig procentuell befolkningsförändring för {country_name}')
    plt.xticks(rotation=45)
    
    # Höger y-axel för antal invånare
    ax2 = plt.twinx()
    ax2.plot(years, [country_data[year] for year in years], marker='o', label='Folkmängd', color='green')
    ax2.set_ylabel('Folkmängd', color='green')
    
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.show()

def plot_annual_population_change(df, country_name):
    # Filtrera DataFrame för det valda landet
    country_data = df[df['Country Name'].str.lower() == country_name.lower()]
    if country_data.empty:
        print(f"Landet '{country_name}' hittades inte.")
        return

    country_data = country_data.iloc[0]  # Ta första raden om det finns flera
    years = [str(year) for year in range(1961, 2022)]
    population_values = country_data[years].values
    population_changes = [(population_values[i] - population_values[i - 1]) / population_values[i - 1] * 100 
                          for i in range(1, len(population_values))]

    # Skapa linjediagram för den procentuella befolkningsförändringen
    plt.figure(figsize=(15, 8))
    plt.plot(years[1:], population_changes, label='Procentuell befolkningsförändring', color='blue')
    plt.xlabel('År')
    plt.ylabel('Procentuell befolkningsförändring', color='blue')
    plt.title(f'Årlig procentuell befolkningsförändring för {country_name} (1961-2021)')
    plt.xticks(rotation=45)
    plt.grid(True)

    # Höger y-axel för antalet invånare
    ax2 = plt.twinx()
    ax2.plot(years, population_values, label='Antal invånare', color='green')
    ax2.set_ylabel('Antal invånare', color='green')
    
    # Visa båda linjediagrammen
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.show()

# Beräkna befolkningsförändringen
# df_population_change = calculate_population_change(df_worldpubind, '1960', '2021')

# Visa länderna med störst förändring
# plot_population_change(df_population_change)

# Fråga användaren efter ett land och visa den årliga förändringen
# country_input = input("Ange ett landsnamn för att se dess befolkningsförändring: ")
# plot_annual_population_change(df_worldpubind, country_input)



# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 5
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:
def analyze_and_plot_city_data(df):
    # Säkerställ att befolkningskolumnen är numerisk och ta bort rader med NaN i 'population'
    df['population'] = pd.to_numeric(df['population'], errors='coerce')
    df.dropna(subset=['population'], inplace=True)

    # Räkna antal städer per land
    cities_per_country = df['country'].value_counts().rename_axis('country').reset_index(name='number_of_cities')

    # Hitta den största staden per land
    largest_cities = df.loc[df.groupby('country')['population'].idxmax()]

    # Sammanfoga data för att få den största staden och dess befolkningsstorlek per land
    cities_data = pd.merge(cities_per_country, largest_cities[['country', 'city', 'population']], on='country')

    # Välj de 10 översta posterna efter antal städer
    top_cities_data = cities_data.head(10).sort_values('number_of_cities', ascending=False)

    # Skriv ut tabellen
    print(top_cities_data)

    # Första stapeldiagram för antal städer per land
    plt.figure(figsize=(12, 6))
    plt.bar(top_cities_data['country'], top_cities_data['number_of_cities'], color='skyblue')
    plt.title('Antal städer per land')
    plt.xlabel('Land')
    plt.ylabel('Antal städer')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Andra stapeldiagram för största stad och befolkning
    plt.figure(figsize=(12, 6))
    plt.bar(top_cities_data['city'], top_cities_data['population'], color='orange')
    plt.title('Största staden och befolkning per land')
    plt.xlabel('Stad')
    plt.ylabel('Befolkning')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

#analyze_and_plot_city_data(df_worldcities)
    
# Alla uppgifter:

def main():
    while True:
        print("\nSkriv vilken uppgift du vill se lösnigen på")
        print("Välj ett alternativ: 2, 3, 4a, 4b, 5 eller q för att avsluta programmet")
        
    
        choice = input("Ange ditt val: ")
    
        if choice == '2':
            input_value = input("Ange antal länder (med + för högst och - för lägst) eller ett landsnamn: ")
            plot_density(df_cia_factbook, input_value)
        elif choice == '3':
            menu()
        elif choice == '4a':
            df_population_change = calculate_population_change(df_worldpubind, '1960', '2021')
            plot_population_change(df_population_change)
        elif choice == '4b':
            country_input = input("Ange ett landsnamn för att se dess befolkningsförändring: ")
            plot_annual_population_change(df_worldpubind, country_input)
        elif choice == '5':
            analyze_and_plot_city_data(df_worldcities)
        elif choice == 'q':
            print("Avslutar programmet...")
            break
        else:
            print("Ogiltigt val, försök igen.")

main()