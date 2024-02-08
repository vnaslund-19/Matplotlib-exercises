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
df_cia_factbook['density'] = df_cia_factbook['population'] / df_cia_factbook['area']

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
    
    print(filtered_countries[['country', 'area', 'birth_rate', 'life_exp_at_birth']])

def menu_option_2(df):
    df['internet_user_density'] = (df['internet_users'] / df['population']) * 100000
    sorted_df = df.sort_values('internet_user_density')
    filtered_countries = pd.concat([sorted_df.head(5), sorted_df.tail(5)])
    
    print(filtered_countries[['country', 'population', 'internet_user_density']])

def menu_option_3(df):
    df['population_growth_rate'] = (df['birth_rate'] - df['death_rate'] + df['net_migration_rate'])
    df['population_change'] = df['population_growth_rate']  # Redan i procent per 1000 invånare
    
    sorted_df = df.sort_values('population_change')
    filtered_countries = pd.concat([sorted_df.head(5), sorted_df.tail(5)])
    
    print(filtered_countries[['country', 'birth_rate', 'death_rate', 'net_migration_rate', 'population_change']])
    
    # Stapeldiagram
    plt.figure(figsize=(10, 8))
    plt.bar(filtered_countries['country'], filtered_countries['population_change'], color='skyblue')
    plt.xlabel('Länder')
    plt.ylabel('Befolkningsförändring')
    plt.xticks(rotation=45, ha="right")
    plt.title('Befolkningsförändring per Land')
    plt.tight_layout()
    plt.show()


while True:
    print("\nVälj ett alternativ:")
    print("1: Visa länder enligt specifika kriterier")
    print("2: Visa länder baserat på internetanvändare per 100.000 invånare")
    print("3: Visa länder med mest positiv och negativ befolkningsförändring")
    print("4: Avsluta programmet")
    
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




# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 4
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här: