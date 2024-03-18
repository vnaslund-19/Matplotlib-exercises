# uppgift 3:
# ----------
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# ------------ Uppgift A ------------
df_cia_factbook = pd.read_csv('cia_factbook.csv', sep=';')

print("# --------- Uppgift B ---------")
# Skapa 'density' kolumnen
df_cia_factbook['density'] = df_cia_factbook['population'] / df_cia_factbook['area']

# Ta bort rader där 'density' är inf eller NaN
df_cia_factbook = df_cia_factbook[df_cia_factbook['density'].notna() & ~df_cia_factbook['density'].isin([float('inf'), -float('inf')])]

def plot_countries(num_or_country):
    if num_or_country.endswith('+'):
        num = int(num_or_country[:-1])
        sorted_df = df_cia_factbook.sort_values(by='density', ascending=False).head(num)
    elif num_or_country.endswith('-'):
        num = int(num_or_country[:-1])
        sorted_df = df_cia_factbook.sort_values(by='density', ascending=True).head(num)
    else: #Skriv ut ett specifikt land
        country_density = df_cia_factbook.loc[df_cia_factbook['country'].str.lower() == num_or_country.lower(), 'density']
        if not country_density.empty:
            print(f"Befolkningstäthet för {num_or_country}: {country_density.values[0]} inv/km2")
            return
        else:
            print(f"Landet '{num_or_country}' hittades inte.")
            return

    plt.figure(figsize=(10, 6))
    plt.bar(sorted_df['country'], sorted_df['density'])
    plt.xlabel('Länder')
    plt.ylabel('Befolkningstäthet (inv/km2)')
    plt.title('Befolkningstäthet per Land')
    plt.xticks(rotation=45)
    plt.show()

def get_user_input():
    while True:
        user_input = input("Ange antal länder (med '+' eller '-') eller ett specifikt lands namn: ")
        if user_input.endswith('+') or user_input.endswith('-'):
            # Kontrollerar om det är ett giltigt nummer följt av + eller -
            try:
                num = int(user_input[:-1])
                if 1 <= num <= 10:
                    return user_input
                else:
                    print("Ange ett nummer mellan 1 och 10.")
            except ValueError:
                print("Ogiltig inmatning. Ange ett nummer följt av '+' eller '-'.")
        elif any(df_cia_factbook['country'].str.lower() == user_input.lower()):
            # Kontrollerar om det angivna landet finns i datasetet
            return user_input
        else:
            print(f"Landet '{user_input}' hittades inte eller ogiltig inmatning.")

user_input = get_user_input()
plot_countries(user_input)

print("\n# --------- Uppgift C ---------")
def menu_option_1():
    filtered_countries = df_cia_factbook[(df_cia_factbook['population'] > df_cia_factbook['population'].mean()) &
                                          (df_cia_factbook['area'] < df_cia_factbook['area'].mean()) &
                                          (df_cia_factbook['birth_rate'].between(15, 24)) &
                                          (df_cia_factbook['life_exp_at_birth'] > 70)]
    print(filtered_countries[['country', 'area', 'birth_rate', 'life_exp_at_birth']].to_string(index=False, float_format='{:0.0f}'.format))

def menu_option_2():
    # Skapar en ny kolumn internet_user_density som beräknar antalet internetanvändare per 100 000 invånare
    df_cia_factbook['internet_user_density'] = df_cia_factbook['internet_users'] / (df_cia_factbook['population'] / 100000)
    filtered_countries = df_cia_factbook.dropna(subset=['internet_user_density'])
    smallest = filtered_countries.nsmallest(5, 'internet_user_density')
    largest = filtered_countries.nlargest(5, 'internet_user_density')
    
    print("{:<35} {:<15} {:<30}".format("Land", "Folkmängd", "Internetanvändare [per 100k]"))
    print("-" * 75)

    print("Länder med lägst antal internetanvändare per 100.000 invånare:")
    for _, row in smallest.iterrows():
        print(f"{row['country']:<35} {row['population']:<15.0f} {row['internet_user_density']:<30.1f}")

    print("\nLänder med högst antal internetanvändare per 100.000 invånare:")
    for _, row in largest.iterrows():
        print(f"{row['country']:<35} {row['population']:<15.0f} {row['internet_user_density']:<30.1f}")


def menu_option_3():
    # Beräknar befolkningsförändringshastigheten
    df_cia_factbook['population_growth_rate'] = df_cia_factbook['birth_rate'] - df_cia_factbook['death_rate'] + df_cia_factbook['net_migration_rate']

    # Beräknar den absoluta befolkningsförändringen
    df_cia_factbook['population_change'] = (df_cia_factbook['population_growth_rate'] / 1000) * df_cia_factbook['population']
    filtered_countries = df_cia_factbook.dropna(subset=['population_change'])
    largest_pos = filtered_countries.nlargest(5, 'population_change').sort_values('population_change', ascending=False)
    smallest_neg = filtered_countries.nsmallest(5, 'population_change').sort_values('population_change', ascending=True)
    
    print("{:<30} {:<15} {:<15} {:<20} {:<30}".format("Land", "Födslar[per 1k]", "Döda[per 1k]", "Migration[per 1k]", "Befolkningsföränding[%]"))
    print("-" * 95)

    print("Länder med mest negativ befolkningstrend:")
    for _, row in smallest_neg.iterrows():
        print("{:<20} {:<15.0f} {:<15.0f} {:<20.0f} {:<30.2f}".format(row['country'], row['birth_rate'], row['death_rate'], row['net_migration_rate'], row['population_change']))

    print("\nLänder med mest positiv befolkningstrend:")
    for _, row in largest_pos.iterrows():
        print("{:<20} {:<15.0f} {:<15.0f} {:<20.0f} {:<30.2f}".format(row['country'], row['birth_rate'], row['death_rate'], row['net_migration_rate'], row['population_change']))

    plt.figure(figsize=(10, 6))
    countries = list(smallest_neg['country']) + list(largest_pos['country'])
    population_changes = list(smallest_neg['population_change']) + list(largest_pos['population_change'])
    plt.bar(countries, population_changes, color=['red'] * 5 + ['blue'] * 5)
    plt.grid(True)
    plt.ylabel("Befolkningsförändring '%' av folkmängd")
    plt.title('Länder med minst och störst befolkningsökning3')
    plt.xticks(rotation=45, ha='right')

    def percent_formatter(x, pos):
        return f"{x/1000000:.1f}"  #Formatterar till %

    plt.gca().yaxis.set_major_formatter(FuncFormatter(percent_formatter))

    plt.tight_layout()
    plt.show()

while True:
        print("\nHuvudmeny:")
        print("1. Visa länder enligt specifika kriterier.")
        print("2. Analysera internetmognaden.")
        print("3. Analysera befolkningstrender.")
        print("4. Avsluta programmet.")
        
        val = input("Välj ett alternativ (1-4): ")
        
        if val == '1':
            menu_option_1()
        elif val == '2':
            menu_option_2()
        elif val == '3':
            menu_option_3()
        elif val == '4':
            print("Avslutar programmet.")
            break
        else:
            print("Ogiltigt val, försök igen.")