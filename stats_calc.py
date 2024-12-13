import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

# Les data
df = pd.read_csv('Nr_8_Zonal_stats.csv')

# Konverter relTreeArea til prosent
df['relTreeArea'] = df['relTreeArea'] * 100

# Beregn differanse
df['differanse'] = df['relTreeArea'] - df['_mean']

# Grunnleggende statistikk
print("Grunnleggende statistikk:")
print("------------------------")
print("Gjennomsnittlig differanse:", df['differanse'].mean())
print("Median differanse:", df['differanse'].median())
print("Standardavvik:", df['differanse'].std())

# Korrelasjon
korrelasjon = df['relTreeArea'].corr(df['_mean'])
print(f"\nPearson korrelasjon: {korrelasjon}")

# Print verdiområder for å verifisere
print("\nVerdiområder etter konvertering:")
print(f"relTreeArea range: {df['relTreeArea'].min():.1f}% - {df['relTreeArea'].max():.1f}%")
print(f"HRL TCD range: {df['_mean'].min():.1f}% - {df['_mean'].max():.1f}%")

# Visualiseringer
# 1. Scatter plot
plt.style.use("seaborn-v0_8")
plt.figure(figsize=(10,6))
sns.scatterplot(data=df, x='relTreeArea', y='_mean', alpha=0.5)
plt.plot([0, 100], [0, 100], 'r--')  # 1:1 linje
plt.xlabel('relTreeArea (%)')
plt.ylabel('HRL TCD (%)')
plt.title('Sammenligning av relTreeArea og HRL TCD')
plt.show()

# 2. Histogram over differanser
plt.figure(figsize=(10,6))
sns.histplot(data=df, x='differanse', bins=50)
plt.xlabel('Differanse (relTreeArea - HRL TCD)')
plt.ylabel('Antall polygoner')
plt.title('Fordeling av differanser mellom relTreeArea og HRL TCD')
plt.show()