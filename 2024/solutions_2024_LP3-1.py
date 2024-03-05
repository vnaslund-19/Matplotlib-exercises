import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 1
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:

df_cpi = pd.read_csv('cpi.csv', delimiter=';')

df_regions = pd.read_csv('regions.csv', delimiter=';')

# Skiljetecknet sätts automatiskt till ',' om inget specificeras
df_inflation = pd.read_csv('inflation.csv')

df_cpi_extended = pd.merge(df_regions[['Land', 'Landskod', 'Kontinent']], df_cpi, on='Landskod')



# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 2
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:

def plot_cpi_for_countries(df, possible_countries):
    countries = [country for country in possible_countries if country in df['Land'].values]
    
    # Kontrollera om listan med existerande länder är tom efter rensning
    if not countries:
        print("Ingen giltig data hittades för de angivna länderna. Ingen graf visas.")
        return

    try:
        plt.figure(figsize=(14, 7))
        for country in countries:
            country_data = df[df['Land'] == country]
            years = list(map(str, range(1960, 2023))) 
            cpi_values = country_data.iloc[0][years].dropna().astype(float) # Radera ogiltig data

            if len(years) != len(cpi_values):
                print(f"Nödvändig data saknas för {country}.")
                continue  # Hoppar över den här iterationen och fortsätter med nästa land
    
            plt.plot(years, cpi_values, label=country)
    
            # Markera största och minsta värdet
            max_value = cpi_values.max()
            min_value = cpi_values.min()
            max_year = cpi_values.idxmax()
            min_year = cpi_values.idxmin()
    
            plt.scatter(max_year, max_value, color='red')  
            plt.scatter(min_year, min_value, color='blue')
        
        plt.title('Inflation under tidsperioden 1960-2022')
        plt.xlabel('År')
        plt.ylabel('CPI')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"Ett fel uppstod: {e}")

def plot_inflation_change_factor(df, country):
    print(f"Plotting change factor for: {country}")
    # Gör om både användarens input och 'Land'-kolumnen till små bokstäver för jämförelse
    country_lowercase = country.lower()
    if country_lowercase in df['Land'].str.lower().values:
        country_data = df[df['Land'].str.lower() == country_lowercase]
        years = list(map(str, range(1960, 2023)))
        try:
            inflation_values = country_data.iloc[0][years].astype(float).values
            change_factors = [(inflation_values[i] - inflation_values[i - 1]) / inflation_values[i - 1] * 100 
                              for i in range(1, len(inflation_values))] # Kalkyl för förändringsfaktorer
            plt.figure(figsize=(14, 7))
            plt.bar(years[1:], change_factors, color='skyblue')
            plt.title(f'Inflation Change Factors for {country.title()} (1961-2022)')
            plt.xlabel('År')
            plt.ylabel('Förändringsfaktor (%)')
            plt.xticks(rotation=90)
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"Error plotting change factor for {country}: {e}")
    else:
        print(f"No data found for {country}")

# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 3
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:

def analyze_inflation_by_year(df, year):
    # Kontrollera att året finns som en kolumn i DataFrame
    if str(year) not in df.columns:
        print(f"Data för året {year} finns inte.")
        return

    # Filtrera bort länder utan data för det angivna året
    df_year = df.dropna(subset=[str(year)])
    
    # Sortera för att hitta de sex länderna med lägst och högst inflation
    lowest_inflation = df_year.nsmallest(6, str(year))
    highest_inflation = df_year.nlargest(6, str(year))
    
    max_country_len = max(lowest_inflation['Land'].apply(len).max(), highest_inflation['Land'].apply(len).max())

    print(f"{'Lägst inflation':<{max_country_len + 20}}{'Högst inflation'}")

    # Iterera över raderna i båda DataFrame för att skriva ut sida vid sida
    for (low_index, low_row), (high_index, high_row) in zip(lowest_inflation.iterrows(), highest_inflation.iterrows()):
        country_low = low_row['Land']
        inflation_low = f"{low_row[str(year)]:.1f}"
        country_high = high_row['Land']
        inflation_high = f"{high_row[str(year)]:.1f}"
        print(f"{country_low:<{max_country_len + 10}}{inflation_low:<10}{country_high:<{max_country_len + 10}}{inflation_high:<10}")
    
    
    combined_inflation = pd.concat([lowest_inflation, highest_inflation]).sort_values(by=str(year))
    
    
    # Rita stapeldiagram
    plt.figure(figsize=(14, 7))
    
    # Plotta kombinerat diagram
    plt.bar(combined_inflation['Land'], combined_inflation[str(year)], color=['green']*6 + ['red']*6)
    
    plt.title(f'Inflation för år {year}')
    plt.xlabel('Land')
    plt.ylabel('Inflation (%)')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()
    
# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 4
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:

def analyze_inflation_by_continent(df_cpi, df_regions):
    # Konvertera årskolumner till numerisk typ och smält dataframe till ett långt format och
    # Omvandla 'wide' format data (en kolumn per år) till 'long' format (en rad per år och landskod)
    years = [str(year) for year in range(1960, 2023)]
    df_cpi_long = df_cpi.melt(id_vars='Landskod', value_vars=years, var_name='År', value_name='Inflation')
    df_cpi_long['Inflation'] = pd.to_numeric(df_cpi_long['Inflation'], errors='coerce')
    df_cpi_long['År'] = df_cpi_long['År'].astype(int)

    # Sammanfoga df_cpi_long och df_regions för att inkludera 'Land' och 'Kontinent'
    df_merged = pd.merge(df_cpi_long, df_regions, on='Landskod')

    # Beräkna medelinflationen per kontinent
    mean_inflation = df_merged.groupby('Kontinent')['Inflation'].mean().reset_index(name='Kontinent avg[%]')

    # Hitta de tre högsta och lägsta inflationerna per kontinent
    top_inflations = df_merged.sort_values('Inflation', ascending=False).groupby('Kontinent').head(3)
    bottom_inflations = df_merged.sort_values('Inflation').groupby('Kontinent').head(3)

    # Sammanfoga dessa med mean_inflation för att få en enda dataframe
    extremes = pd.concat([top_inflations, bottom_inflations], axis=0)

    # Sortera för att få en snygg output
    extremes_sorted = extremes.sort_values(by=['Kontinent', 'Inflation'], ascending=[True, False])
    
    # Skapa en output dataframe som inkluderar medelinflationen för kontinenten
    output = pd.merge(mean_inflation, extremes_sorted, on='Kontinent', how='outer')

    # Sortera och organisera kolumnerna
    output = output[['Kontinent', 'Land', 'År', 'Inflation', 'Kontinent avg[%]']]
    output.sort_values(by=['Kontinent', 'Inflation'], ascending=[True, False], inplace=True)
    
    print(output.to_string(index=False))


# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 5
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:
    
def plot_inflation(df_inflation, df_regions):
    # Lägg till en kolumn 'COUNTRY' i df_inflation baserat på df_regions
    df_inflation = pd.merge(df_inflation, df_regions[['Landskod', 'Land']], left_on='LOCATION', right_on='Landskod')
    df_inflation.rename(columns={'Land': 'COUNTRY'}, inplace=True)

    country_input = input("Ange vilket land som ska analyseras: ")
    subject_input = input("Ange vilken subject du vill analysera: ")
    frequency_input = input("Ange vilken frequency du vill analysera: ")
    measure_input = input("Ange vilken measure du vill analysera: ")
    
    # Filtrera data baserat på användarinmatningen
    df_filtered = df_inflation[
        (df_inflation['COUNTRY'].str.upper() == country_input.upper()) &
        (df_inflation['SUBJECT'].str.upper() == subject_input.upper()) &
        (df_inflation['FREQUENCY'].str.upper() == frequency_input.upper()) &
        (df_inflation['MEASURE'].str.upper() == measure_input.upper())
    ]
    
    # Sortera efter 'TIME' för att säkerställa rätt ordning i plotten
    df_filtered = df_filtered.sort_values(by='TIME')

    # Hitta de fem högsta och lägsta värdena
    top_5 = df_filtered.nlargest(5, 'Value')
    bottom_5 = df_filtered.nsmallest(5, 'Value')
    
    # Plotta linjediagrammet
    plt.figure(figsize=(10, 6))
    plt.plot(df_filtered['TIME'], df_filtered['Value'], label='Inflation', marker='', color='blue', linestyle='-')
    plt.scatter(top_5['TIME'], top_5['Value'], color='red', label='Top 5', zorder=5)
    plt.scatter(bottom_5['TIME'], bottom_5['Value'], color='green', label='Bottom 5', zorder=5)
    
    # Lägg till titel och etiketter
    plt.title(f'Inflation för {country_input} - {subject_input} - {measure_input}')
    plt.xlabel('År')
    plt.ylabel('Inflation (%)')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

# Main funktion för att köra koden till uppgifter 2-5
def main():
    while True:
        print("\nSkriv vilken uppgift du vill se lösnigen på")
        print("Välj ett alternativ: 2a, 2b, 3, 4, 5 eller q för att avsluta programmet")
        
    
        choice = input("Ange ditt val: ")
    
        if choice == '2a':
            # Samla in länder för CPI-trendanalys
            countries_to_analyze = []
            print("Ange upp till 3 länder för CPI-trendanalys eller 'END' för att fortsätta.")
            while len(countries_to_analyze) < 3:
                country_name = input("Ange namnet på landet som du vill analysera: ")
                if country_name.upper() == 'END':
                    break
                countries_to_analyze.append(country_name)
            # Plotta CPI för de valda länderna om något existerar (input måste matcha landets namn i .csv filen exakt)
            if countries_to_analyze:
                plot_cpi_for_countries(df_cpi_extended, countries_to_analyze)
        elif choice == '2b':
            change_factor_country = input("Ange namnet på landet som du vill analysera förändringsfaktorn för: ")
            if df_cpi_extended['Land'].str.contains(change_factor_country, case=False).any():
                plot_inflation_change_factor(df_cpi_extended, change_factor_country)
            else:
                print("Landet hittades inte för förändringsfaktoranalysen.")
        elif choice == '3':
            year_to_analyze = input("Ange vilket år som ska analyseras: ")
            try:
                year_to_analyze = int(year_to_analyze)
                analyze_inflation_by_year(df_cpi_extended, year_to_analyze)
            except ValueError:
                print("Du måste ange ett giltigt år.")
        elif choice == '4':
            analyze_inflation_by_continent(df_cpi, df_regions)
        elif choice == '5':
            plot_inflation(df_inflation, df_regions)
        elif choice == 'q':
            print("Avslutar programmet...")
            break
        else:
            print("Ogiltigt val, försök igen.")

main()
