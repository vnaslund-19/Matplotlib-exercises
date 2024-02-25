import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 1
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:

df_cpi = pd.read_csv('cpi.csv', delimiter=';')

df_regions = pd.read_csv('regions.csv', delimiter=';')

# Skiljetecknet sätts automatiskt till ',' om inget specificeras
df_inflation = pd.read_csv('inflation.csv')




# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 2
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:
df_cpi_extended = pd.merge(df_regions[['Land', 'Landskod', 'Kontinent']], df_cpi, on='Landskod')

def plot_cpi_for_countries(df, countries):
    existing_countries = [country for country in countries if country in df['Land'].values]
    
    # Kontrollera om listan med existerande länder är tom efter borttagning
    if not existing_countries:
        print("Ingen giltig data hittades för de angivna länderna. Ingen graf visas.")
        return

    try:
        plt.figure(figsize=(14, 7))
        for country in existing_countries:
            country_data = df[df['Land'] == country]
            years = list(map(str, range(1960, 2023)))
            cpi_values = country_data.iloc[0][years].values
            
            plt.plot(years, cpi_values, label=country, marker='o')
        
        plt.title('Inflation under tidsperioden 1960-2022')
        plt.xlabel('År')
        plt.ylabel('CPI')
        if existing_countries:  # Kontrollera om det finns länder att lägga till i legenden
            plt.legend()
        plt.grid(True)
        plt.xticks(rotation=90)  # Roterar årtalen vertikalt
        plt.tight_layout()  # Justerar layouten så att allt får plats
        plt.show()
    except Exception as e:
        print(f"Ett fel uppstod: {e}")

def plot_inflation_change_factor(df, country):
    print(f"Plotting change factor for: {country}")
    # Gör om både användarens input och 'Land'-kolumnen till små bokstäver för jämförelse
    country_lowercase = country.lower()
    if country_lowercase in df['Land'].str.lower().values:
        country_data = df[df['Land'].str.lower() == country_lowercase]
        years = list(map(str, range(1961, 2023)))
        try:
            inflation_values = country_data.iloc[0][years].astype(float).values
            change_factors = [(inflation_values[i] - inflation_values[i - 1]) / inflation_values[i - 1] * 100 
                              for i in range(1, len(inflation_values))]
            plt.figure(figsize=(14, 7))
            plt.bar(years[1:], change_factors, color='skyblue')
            plt.title(f'Inflation Change Factors for {country.title()} (1961-2022)')  # Använd 'title()' för att normalisera utseendet på landets namn
            plt.xlabel('År')
            plt.ylabel('Förändringsfaktor (%)')
            plt.xticks(rotation=90)  # Roterar årtalen vertikalt
            plt.tight_layout()  # Justerar layouten så att allt får plats
            plt.show()
        except Exception as e:
            print(f"Error plotting change factor for {country}: {e}")
    else:
        print(f"No data found for {country}")
"""
# Samla in länder för CPI-trendanalys
countries_to_analyze = []
print("Ange upp till 3 länder för CPI-trendanalys eller 'END' för att fortsätta.")
while len(countries_to_analyze) < 3:
    country_name = input("Ange namnet på landet som du vill analysera: ")
    if country_name.upper() == 'END':
        break
    if df_cpi_extended['Land'].str.contains(country_name, case=False).any():
        countries_to_analyze.append(country_name)
    else:
        print("Landet hittades inte, försök igen.")

# Plotta CPI för de valda länderna
if countries_to_analyze:
    plot_cpi_for_countries(df_cpi_extended, countries_to_analyze)

# Fråga användaren efter ett specifikt land för förändringsfaktoranalysen
change_factor_country = input("Ange namnet på landet som du vill analysera förändringsfaktorn för: ")
if df_cpi_extended['Land'].str.contains(change_factor_country, case=False).any():
    plot_inflation_change_factor(df_cpi_extended, change_factor_country)
else:
    print("Landet hittades inte för förändringsfaktoranalysen.")
"""
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
    
    # Kombinera de två dataramarna och sortera dem från lägst till högst inflation
    combined_inflation = pd.concat([lowest_inflation, highest_inflation]).sort_values(by=str(year))
    
    # Presentera resultaten i tabellform
    print(f"Länder med lägst inflation år {year}:")
    print(lowest_inflation[['Land', str(year)]].to_string(index=False))
    print(f"Länder med högst inflation år {year}:")
    print(highest_inflation[['Land', str(year)]].to_string(index=False))
    
    # Rita stapeldiagram
    plt.figure(figsize=(14, 7))
    
    # Plotta kombinerat diagram
    plt.bar(combined_inflation['Land'], combined_inflation[str(year)], color=['skyblue']*6 + ['darkorange']*6)
    
    plt.title(f'Inflation för år {year}')
    plt.xlabel('Land')
    plt.ylabel('Inflation (%)')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

"""
# Använd funktionen
year_to_analyze = input("Ange vilket år som ska analyseras: ")
try:
    year_to_analyze = int(year_to_analyze)
    analyze_inflation_by_year(df_cpi_extended, year_to_analyze)
except ValueError:
    print("Du måste ange ett giltigt år.")
"""
    
# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 4
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:

def analyze_inflation_by_continent(df_cpi, df_regions):
    # Merge CPI data with region data to get continent information for each country
    df_merged = pd.merge(df_cpi, df_regions[['Landskod', 'Kontinent', 'Land']], on='Landskod', how='left')

    # Create an empty DataFrame to store the results
    results = pd.DataFrame()

    # Calculate statistics for each continent
    for continent in df_merged['Kontinent'].dropna().unique():
        continent_df = df_merged[df_merged['Kontinent'] == continent]

        # Calculate the mean inflation for each continent over the years
        mean_inflation = continent_df.iloc[:, 2:-2].mean(axis=1).mean()

        # Find the years with the highest and lowest inflation
        highest_inf = continent_df.iloc[:, 2:-2].max(axis=1)
        highest_years = highest_inf.idxmax(axis=1)
        highest_countries = continent_df.loc[highest_inf.idxmax(), 'Land']

        lowest_inf = continent_df.iloc[:, 2:-2].min(axis=1)
        lowest_years = lowest_inf.idxmin(axis=1)
        lowest_countries = continent_df.loc[lowest_inf.idxmin(), 'Land']

        # Construct the result row
        result_row = {
            'Kontinent': continent,
            'Högst Inf [%]': highest_inf.max(),
            'Högst År': highest_years[highest_inf.idxmax()],
            'Högst Land': highest_countries.iloc[0],
            'Lägst Inf [%]': lowest_inf.min(),
            'Lägst År': lowest_years[lowest_inf.idxmin()],
            'Lägst Land': lowest_countries.iloc[0],
            'Medel Inf [%]': mean_inflation
        }

        # Append the result
        results = results.append(result_row, ignore_index=True)

    # Format the results to match the example's layout
    results = results[['Kontinent', 'Högst Land', 'Högst Inf [%]', 'Högst År', 'Lägst Land', 'Lägst Inf [%]', 'Lägst År', 'Medel Inf [%]']]
    print(results.to_string(index=False))

analyze_inflation_by_continent(df_cpi, df_regions)




# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 5
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:



