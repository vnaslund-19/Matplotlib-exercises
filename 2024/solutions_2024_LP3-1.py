import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib import colormaps

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
    # Konvertera årskolumner till numerisk typ och smält dataframe till ett långt format
    years = [str(year) for year in range(1960, 2023)]
    df_cpi_long = df_cpi.melt(id_vars='Landskod', value_vars=years, var_name='År', value_name='Inflation')
    df_cpi_long['Inflation'] = pd.to_numeric(df_cpi_long['Inflation'], errors='coerce')
    df_cpi_long['År'] = df_cpi_long['År'].astype(int)

    # Sammanfoga df_cpi_long och df_regions för att inkludera 'Land' och 'Kontinent'
    df_merged = pd.merge(df_cpi_long, df_regions, on='Landskod')

    # Beräkna medelinflation per kontinent
    continent_means = df_merged.groupby('Kontinent')['Inflation'].mean().reset_index()
    continent_means['Inflation'] = continent_means['Inflation'].round(1)

    # Hitta topp 3 högsta och lägsta inflationer per kontinent och år
    top3 = df_merged.groupby('Kontinent')['Inflation'].nlargest(3).reset_index()
    top3_extreme = df_merged.loc[top3['level_1']]
    bottom3 = df_merged.groupby('Kontinent')['Inflation'].nsmallest(3).reset_index()
    bottom3_extreme = df_merged.loc[bottom3['level_1']]

    # Skapa en tabell för presentation
    table = ""

    indentation = ' ' * 20
    for continent in continent_means['Kontinent']:
        mean_inflation = continent_means.loc[continent_means['Kontinent'] == continent, 'Inflation'].item()
        table += f"{indentation}{continent}\n"
        table += f"{'Kontinent avg[%]:':<10} {mean_inflation}\n"
        table += f"{indentation}Högsta 3\n"
        table += f"{'Land':<35} {'År':<6} {'Inf[%]':<8}\n"

        # 3 högsta inflationer
        for _, row in top3_extreme[top3_extreme['Kontinent'] == continent].iterrows():
            table += f"{row['Land']:<35} {row['År']:<6} {row['Inflation']:.1f}\n"

        # 3 lägsta inflationer
        table += f"{indentation}Lägsta 3\n"
        for _, row in bottom3_extreme[bottom3_extreme['Kontinent'] == continent].iterrows():
            table += f"{row['Land']:<35} {row['År']:<6} {row['Inflation']:.1f}\n"
        
        table += "\n" # Lägger till tomrad mellan kontinenter

    # Skriv ut tabellen
    print(table)


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
    
    # Filter data based on user input
    df_filtered = df_inflation[
        (df_inflation['COUNTRY'].str.upper() == country_input.upper()) &
        (df_inflation['SUBJECT'].str.upper() == subject_input.upper()) &
        (df_inflation['FREQUENCY'].str.upper() == frequency_input.upper()) &
        (df_inflation['MEASURE'].str.upper() == measure_input.upper())
    ]
    
    # Sort by 'TIME' to ensure correct order in the plot
    df_filtered = df_filtered.sort_values(by='TIME')

    # Find the five highest and lowest values
    top_5 = df_filtered.nlargest(5, 'Value')
    bottom_5 = df_filtered.nsmallest(5, 'Value')
    
    # Create a color map for the top and bottom values
    # Create a color map for the top and bottom values without using get_cmap
    cmap = colormaps['hsv']
    colors_top = [cmap(i / 10) for i in range(5)]
    colors_bottom = [cmap((i + 5) / 10) for i in range(5)]

    # Plot the line chart
    plt.figure(figsize=(14, 7))
    plt.plot(df_filtered['TIME'], df_filtered['Value'], label='Inflation', marker='', color='blue', linestyle='-')

    # Plot and label the top 5 highest inflation points with unique colors
    for i, (time, value) in enumerate(zip(top_5['TIME'], top_5['Value'])):
        plt.scatter(time, value, color=colors_top[i], label=f'Högsta {time}', zorder=5)

    # Plot and label the bottom 5 lowest inflation points with unique colors
    for i, (time, value) in enumerate(zip(bottom_5['TIME'], bottom_5['Value'])):
        plt.scatter(time, value, color=colors_bottom[i], label=f'Lägsta {time}', zorder=5)

    # Add title and labels with the frequency input included
    plt.title(f'Inflation for {country_input} - {subject_input} - {frequency_input} - {measure_input}')
    plt.xlabel('År')
    plt.ylabel('Inflation (%)')

    # Create a custom legend
    legend_elements = [Line2D([0], [0], color='blue', label='Inflation')]
    legend_elements += [Line2D([0], [0], marker='o', color='w', markerfacecolor=colors_top[i], label=f'Högsta {top_5["TIME"].iloc[i]}') for i in range(len(top_5))]
    legend_elements += [Line2D([0], [0], marker='o', color='w', markerfacecolor=colors_bottom[i], label=f'Lägsta {bottom_5["TIME"].iloc[i]}') for i in range(len(bottom_5))]

    plt.legend(handles=legend_elements, loc='best', ncol=2)

    # Enhance the plot aesthetics
    plt.grid(True)
    plt.xticks(rotation=90)
    plt.tight_layout()

    # Show the plot
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
