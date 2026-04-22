
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import json

df_lokacije = pd.read_csv('mars_lokacije.csv', sep=';', decimal=',')
df_uzorci = pd.read_csv('mars_uzorci.csv', sep=';', decimal=',')

df = pd.merge(df_lokacije, df_uzorci, on='ID_Uzorka')

uvjet_anomalije = (df['Temperatura'] < -80) | (df['Temperatura'] > -30) | (df['Vlaga'] > 6)

df_anomalije = df[uvjet_anomalije]

df_cisto = df[~uvjet_anomalije]

# GRAPH 1: Temperatura i vlaga, ovisno o metanu
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_cisto, x='Temperatura', y='Vlaga', hue='Metan')
plt.title('Odnos temperature i vlage')
plt.savefig('graph1_temp_h2o.png')
plt.close()

# GRAPH 2: Heatmap dubine
plt.figure(figsize=(10, 6))

sns.scatterplot(data=df_cisto, x='GPS_LONG', y='GPS_LAT', hue='Dubina', palette='viridis', size='Dubina')
plt.title('Karta dubine bušenja')
plt.savefig('graph2_heatmap_depth.png')
plt.close()

# GRAPH 3: Očitanja metana
plt.figure(figsize=(10, 6))

sns.scatterplot(data=df_cisto, x='GPS_LONG', y='GPS_LAT', hue='Metan',
                palette={'Pozitivno': 'red', 'Negativno': 'blue'})
plt.title('Prisutnost metana')
plt.savefig('graph3_methane_scatter.png')
plt.close()

# GRAPH 4: Kandidati (Metan + Organske molekule)
plt.figure(figsize=(10, 6))

sns.scatterplot(data=df_cisto, x='GPS_LONG', y='GPS_LAT', hue='Vlaga', alpha=0.5)

kandidati = df_cisto[(df_cisto['Metan'] == 'Pozitivno') & (df_cisto['Organske_molekule'] == True)]

plt.scatter(kandidati['GPS_LONG'], kandidati['GPS_LAT'], marker='*', s=250, color='red', label='Kandidati')
plt.legend()
plt.title('Potencijalni kandidati za bušenje')
plt.savefig('scatter_plot.png')
plt.close()
# GRAPH 5: Jezero Mission Map
plt.figure(figsize=(12, 8))

extent_koordinate = [
    df_cisto['GPS_LONG'].min(), df_cisto['GPS_LONG'].max(),
    df_cisto['GPS_LAT'].min(), df_cisto['GPS_LAT'].max()
]

slika_kratera = plt.imread('jezero_crater_satellite_map.jpg')
plt.imshow(slika_kratera, extent=extent_koordinate, aspect='auto', alpha=0.7)

sns.scatterplot(data=df_cisto, x='GPS_LONG', y='GPS_LAT', color='cyan', alpha=0.5, label='Obična očitanja')
plt.scatter(kandidati['GPS_LONG'], kandidati['GPS_LAT'], marker='*', s=300, color='red', edgecolor='black', label='Kandidati')

plt.title('Satelitska karta kratera Jezero s lokacijama')
plt.legend()
plt.savefig('jezero_mission_map.jpg')
plt.close()
komande_za_rover = []

for index, row in kandidati.iterrows():
    paket_akcija = [
        {"akcija": "NAVIGACIJA", "lokacija": {"lat": row['GPS_LAT'], "long": row['GPS_LONG']}},
        {"akcija": "SONDIRANJE", "dubina_m": row['Dubina']},
        {"akcija": "SLANJE_PODATAKA"}
    ]

    komande_za_rover.append({
        "ID_tocke": row['ID'],
        "zadatci": paket_akcija
    })

payload = {
    "tim": "Karlo_Kazalac",
    "misija": "Jezero_Crater_Drill",
    "nalozi": komande_za_rover
}

api_url = "https://webhook.site/03f33f00-c3a0-4a66-8b06-63f1af147efa"

try:
    response = requests.post(api_url, json=payload)
    print(f"Status koda: {response.status_code}")
    if response.status_code == 200:
        print("Misija uspješna! JSON paket je prihvaćen.")
    else:
        print(f"Greška na serveru. Odgovor: {response.text}")
except Exception as e:
    print(f"Došlo je do greške u komunikaciji: {e}")
