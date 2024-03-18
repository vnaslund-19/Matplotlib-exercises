# uppgift 3:
# ----------
import pandas as pd
import matplotlib.pyplot as plt

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
    else:
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
def menu_option_1(df):
    medel_population = df['population'].mean()
    medel_area = df['area'].mean()
    
    filtered_df = df[(df['population'] > medel_population) &
                     (df['area'] < medel_area) &
                     (df['birth_rate'].between(15, 24)) &
                     (df['life_exp_at_birth'] > 70)]
    
    filtered_df = filtered_df[['country', 'area', 'birth_rate', 'life_exp_at_birth']]
    print(filtered_df.to_string(index=False))

def menu_option_2(df):
    df['internet_user_density'] = df['internet_users'] / (df['population'] / 100000)
    
    lowest_density = df.nsmallest(5, 'internet_user_density')[['country', 'population', 'internet_user_density']]
    highest_density = df.nlargest(5, 'internet_user_density')[['country', 'population', 'internet_user_density']]
    
    combined_df = pd.concat([lowest_density, highest_density])
    print(combined_df.to_string(index=False))

while True:
        print("\nHuvudmeny:")
        print("1. Visa länder enligt specifika kriterier.")
        print("2. Analysera internetmognaden.")
        print("3. Analysera befolkningstrender.")
        print("4. Avsluta programmet.")
        
        val = input("Välj ett alternativ (1-4): ")
        
        if val == '1':
            menu_option_1(df_cia_factbook)
        elif val == '2':
            menu_option_2(df_cia_factbook)
        elif val == '3':
            menu_option_2(df_cia_factbook)
        elif val == '4':
            print("Avslutar programmet.")
            break
        else:
            print("Ogiltigt val, försök igen.")