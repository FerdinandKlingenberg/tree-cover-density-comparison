import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np

# Definer region for hvert datasett
area_regions = {
    'Nr_1_Zonal_stats.csv': 'Nord-Norge (Arctic)',     # Finnmark
    'Nr_2_Zonal_stats.csv': 'Nord-Norge (Sub-Arctic)', # Nordland
    'Nr_3_Zonal_stats.csv': 'Midt-Norge',             # Trøndelag
    'Nr_4_Zonal_stats.csv': 'Midt-Norge',             # Innlandet
    'Nr_5_Zonal_stats.csv': 'Østlandet',              # Akershus
    'Nr_6_Zonal_stats.csv': 'Sørlandet',              # Telemark/Agder
    'Nr_7_Zonal_stats.csv': 'Sørlandet',              # Agder
    'Nr_8_Zonal_stats.csv': 'Sørlandet'               # Rogaland/Vestland
}

# Funksjon for å beregne konfidensintervall (95%)
def konfidensintervall(data):
    confidence = 0.95
    mean = np.mean(data)
    sem = stats.sem(data)
    ci = stats.t.interval(confidence=confidence, 
                         df=len(data)-1,
                         loc=mean,
                         scale=sem)
    return ci

# Les inn alle filer og legg til region
dataframes = []
for file, region in area_regions.items():
    try:
        df = pd.read_csv(file)
        # Konverter relTreeArea til prosent
        df['relTreeArea'] = df['relTreeArea'] * 100
        df['region'] = region
        df['testarea'] = file.replace('_Zonal_stats.csv', '')
        dataframes.append(df)
    except Exception as e:
        print(f"Feil ved lesing av {file}: {e}")

# Kombiner alle datasett
all_data = pd.concat(dataframes, ignore_index=True)

# Beregn differanse
all_data['differanse'] = all_data['relTreeArea'] - all_data['_mean']

# REGIONAL ANALYSE
print("\n=== REGIONAL ANALYSE ===")
print("\nStatistikk per region:")
print("----------------------")

regional_stats = pd.DataFrame()
for region in all_data['region'].unique():
    region_data = all_data[all_data['region'] == region]
    ci = konfidensintervall(region_data['differanse'].dropna())
    
    stats_dict = {
        'Differanse (gjennomsnitt)': region_data['differanse'].mean(),
        'Differanse (standardavvik)': region_data['differanse'].std(),
        'Differanse (median)': region_data['differanse'].median(),
        'Differanse (CI nedre)': ci[0],
        'Differanse (CI øvre)': ci[1],
        'relTreeArea (gjennomsnitt)': region_data['relTreeArea'].mean(),
        'relTreeArea (min)': region_data['relTreeArea'].min(),
        'relTreeArea (max)': region_data['relTreeArea'].max(),
        'HRL TCD (gjennomsnitt)': region_data['_mean'].mean(),
        'HRL TCD (min)': region_data['_mean'].min(),
        'HRL TCD (max)': region_data['_mean'].max()
    }
    
    regional_stats[region] = pd.Series(stats_dict)

print(regional_stats.round(2).T)

# INDIVIDUELL ANALYSE
print("\n=== INDIVIDUELL ANALYSE ===")
print("\nStatistikk per testområde:")
print("-------------------------")

testarea_stats = pd.DataFrame()
for area in all_data['testarea'].unique():
    area_data = all_data[all_data['testarea'] == area]
    ci = konfidensintervall(area_data['differanse'].dropna())
    
    stats_dict = {
        'Differanse (gjennomsnitt)': area_data['differanse'].mean(),
        'Differanse (standardavvik)': area_data['differanse'].std(),
        'Differanse (median)': area_data['differanse'].median(),
        'Differanse (CI nedre)': ci[0],
        'Differanse (CI øvre)': ci[1],
        'relTreeArea (gjennomsnitt)': area_data['relTreeArea'].mean(),
        'relTreeArea (min)': area_data['relTreeArea'].min(),
        'relTreeArea (max)': area_data['relTreeArea'].max(),
        'HRL TCD (gjennomsnitt)': area_data['_mean'].mean(),
        'HRL TCD (min)': area_data['_mean'].min(),
        'HRL TCD (max)': area_data['_mean'].max()
    }
    
    testarea_stats[area] = pd.Series(stats_dict)

print(testarea_stats.round(2).T)

# SAMLET STATISTIKK
print("\n=== SAMLET STATISTIKK ===")
total_ci = konfidensintervall(all_data['differanse'].dropna())
print(f"Gjennomsnittlig differanse: {all_data['differanse'].mean():.2f}")
print(f"Median differanse: {all_data['differanse'].median():.2f}")
print(f"Standardavvik: {all_data['differanse'].std():.2f}")
print(f"95% konfidensintervall: [{total_ci[0]:.2f}, {total_ci[1]:.2f}]")
print(f"Pearson korrelasjon: {all_data['relTreeArea'].corr(all_data['_mean']):.3f}")


# Skriv resultatene til fil
with open('treecoverdensity_analyse.txt', 'w', encoding='utf-8') as f:
    # REGIONAL ANALYSE
    f.write("=== REGIONAL ANALYSE ===\n")
    f.write("Statistikk per region:\n")
    f.write("-" * 100 + "\n\n")
    
    # Skriv regional statistikk
    f.write("Regional statistikk for differanser:\n")
    f.write(regional_stats.T[['Differanse (gjennomsnitt)', 'Differanse (standardavvik)', 
                             'Differanse (median)', 'Differanse (CI nedre)', 
                             'Differanse (CI øvre)']].round(2).to_string())
    f.write("\n\n")
    
    f.write("Regional statistikk for relTreeArea:\n")
    f.write(regional_stats.T[['relTreeArea (gjennomsnitt)', 'relTreeArea (min)', 
                             'relTreeArea (max)']].round(2).to_string())
    f.write("\n\n")
    
    f.write("Regional statistikk for HRL TCD:\n")
    f.write(regional_stats.T[['HRL TCD (gjennomsnitt)', 'HRL TCD (min)', 
                             'HRL TCD (max)']].round(2).to_string())
    f.write("\n\n")

    # INDIVIDUELL ANALYSE
    f.write("\n=== INDIVIDUELL ANALYSE ===\n")
    f.write("Statistikk per testområde:\n")
    f.write("-" * 100 + "\n\n")
    
    # Skriv testområde statistikk
    f.write("Testområde statistikk for differanser:\n")
    f.write(testarea_stats.T[['Differanse (gjennomsnitt)', 'Differanse (standardavvik)', 
                             'Differanse (median)', 'Differanse (CI nedre)', 
                             'Differanse (CI øvre)']].round(2).to_string())
    f.write("\n\n")
    
    f.write("Testområde statistikk for relTreeArea:\n")
    f.write(testarea_stats.T[['relTreeArea (gjennomsnitt)', 'relTreeArea (min)', 
                             'relTreeArea (max)']].round(2).to_string())
    f.write("\n\n")
    
    f.write("Testområde statistikk for HRL TCD:\n")
    f.write(testarea_stats.T[['HRL TCD (gjennomsnitt)', 'HRL TCD (min)', 
                             'HRL TCD (max)']].round(2).to_string())
    f.write("\n\n")

    # SAMLET STATISTIKK
    f.write("\n=== SAMLET STATISTIKK ===\n")
    f.write("-" * 100 + "\n")
    f.write(f"Gjennomsnittlig differanse: {all_data['differanse'].mean():.2f}\n")
    f.write(f"Median differanse: {all_data['differanse'].median():.2f}\n")
    f.write(f"Standardavvik: {all_data['differanse'].std():.2f}\n")
    f.write(f"95% konfidensintervall: [{total_ci[0]:.2f}, {total_ci[1]:.2f}]\n")
    f.write(f"Pearson korrelasjon: {all_data['relTreeArea'].corr(all_data['_mean']):.3f}\n")

print("Analyseresultatene er skrevet til 'treecoverdensity_analyse.txt'")


# Plotting
# REGIONAL PLOTS
# 1. Scatter plot med regioner
plt.style.use("seaborn-v0_8")
plt.figure(figsize=(15, 10))
sns.scatterplot(data=all_data, 
                x='relTreeArea', 
                y='_mean', 
                hue='region',
                alpha=0.5)
plt.plot([0, 100], [0, 100], 'r--', label='1:1 linje')
plt.xlabel('relTreeArea (%)')
plt.ylabel('HRL TCD (%)')
plt.title('Sammenligning av relTreeArea og HRL TCD per region')
plt.legend(title='Region', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('scatter_plot_regional.png', dpi=300, bbox_inches='tight')
plt.show()

# 2. Box plot med regioner
plt.figure(figsize=(12, 6))
sns.boxplot(data=all_data, x='region', y='differanse')
plt.xticks(rotation=45)
plt.xlabel('Region')
plt.ylabel('Differanse (relTreeArea - HRL TCD)')
plt.title('Fordeling av differanser per region')
plt.tight_layout()
plt.savefig('boxplot_regional.png', dpi=300, bbox_inches='tight')
plt.show()

# INDIVIDUELLE PLOTS
# 1. Scatter plot med testområder
plt.figure(figsize=(15, 10))
sns.scatterplot(data=all_data, 
                x='relTreeArea', 
                y='_mean', 
                hue='testarea',
                alpha=0.5)
plt.plot([0, 100], [0, 100], 'r--', label='1:1 linje')
plt.xlabel('relTreeArea (%)')
plt.ylabel('HRL TCD (%)')
plt.title('Sammenligning av relTreeArea og HRL TCD per testområde')
plt.legend(title='Testområde', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('scatter_plot_testomrader.png', dpi=300, bbox_inches='tight')
plt.show()

# 2. Box plot med testområder
plt.figure(figsize=(15, 6))
sns.boxplot(data=all_data, x='testarea', y='differanse')
plt.xticks(rotation=45)
plt.xlabel('Testområde')
plt.ylabel('Differanse (relTreeArea - HRL TCD)')
plt.title('Fordeling av differanser per testområde')
plt.tight_layout()
plt.savefig('boxplot_testomrader.png', dpi=300, bbox_inches='tight')
plt.show()

print("\nAnalysen er ferdig. Resultater er lagret i:")
print("- scatter_plot_regional.png")
print("- boxplot_regional.png")
print("- scatter_plot_testomrader.png")
print("- boxplot_testomrader.png")