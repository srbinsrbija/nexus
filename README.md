# 🚀 Izvještaj Misije Nexus: Inženjerska analiza kratera Jezero
## A. Izvršni sažetak (Executive Summary)
Ova tehnička dokumentacija opisuje razvoj i implementaciju analitičkog sustava za autonomni rover u sklopu Misije Nexus. Svrha projekta je procesiranje kompleksnih senzorskih podataka prikupljenih u krateru Jezero na Marsu. Sustav koristi sirove ulazne podatke o GPS koordinatama i kemijskom sastavu tla kako bi identificirao astrobiološki značajne lokacije. Konačni cilj misije je generiranje automatiziranog navigacijskog naloga za bušenje, koji se dostavlja nadzornom poslužitelju putem strukturiranog JSON protokola, osiguravajući preciznost u robotskom istraživanju terena.
##B. Metodologija obrade podataka (Data Wrangling)
Uspjeh misije ovisio je o rigoroznoj obradi podataka pomoću biblioteke Pandas. Primijenjeni su specifični logički uvjeti na DataFrame objekte kako bi se osigurala korelacija između prostornih i telemetrijskih podataka.
Integracija podataka: Spajanje tablica mars_lokacije i mars_uzorci izvršeno je preko primarnog ključa ID_Uzorka koristeći inner join metodu.
Uklanjanje senzorskog šuma: Identificirane su i uklonjene tri vrste anomalija:
Termalne anomalije: Filtriranje vrijednosti iznad 
 koje indiciraju kvar senzora temperature.
Kemijske pogreške: Uklanjanje negativnih pH vrijednosti koje su fizički nekonzistentne s marsovskim tlom.
Logički filtri: Izolacija uzoraka s potvrđenim prisustvom organskih molekula za daljnju prioritetnu obradu.
## C. Geoprostorna analiza i vizualizacija
Vizualni dokazi ključni su za potvrdu ispravnosti modela kretanja rovera.
1. Distribucija metana i GPS mapiranje

Interpretacija: Grafikon prikazuje prostornu rasprostranjenost uzoraka. Koncentracija crvenih markera ukazuje na klastere metana u blizini delte, što predstavlja primarni cilj misije.
2. Korelacija termodinamičkih parametara

Interpretacija: Scatter plot korelira vlagu i temperaturu tla. Stabilni uvjeti u donjem desnom kvadrantu koreliraju s najvišim razinama vlage, sugerirajući potencijalne podzemne rezervoare.
3. Satelitska karta i Extent mapiranje

Tehnički koncept extent mapiranja korišten je za precizno preklapanje raspršenih podataka na satelitsku snimku visoke rezolucije. Definiranjem rubnih GPS granica (






), sustav vrši transformaciju piksela u stvarne geografske koordinate, omogućujući pouzdanu orijentaciju i izbjegavanje opasnih terenskih prepreka unutar kratera.
## D. Komunikacijski protokol (JSON Uplink)
Sustav automatizirano generira naloge koristeći iterativne petlje koje analiziraju filtrirane podatke, izbjegavajući rizik od ljudske pogreške pri ručnom upisu (hardcoding).
Primjer ugniježđenog JSON niza:
{
  "ID_Uzorka": 123,
  "GPS": {"LAT": 18.48, "LONG": 77.39},
  "Mjerenja": {
    "Vlaga": 5.4,
    "Metan": "Pozitivno",
    "Organske_Molekule": "Da"
  }
}

## E. Inženjerski dnevnik (Troubleshooting Log)
Problem s učitavanjem: CSV datoteke su inicijalno javljale grešku u strukturi. Rješenje je bilo uvođenje parametara sep=';' i decimal=',' unutar read_csv funkcije, jer standardni zarez nije bio separator.
Problem s memorijom/tipovima: ID_Uzorka je morao biti osiguran kao cjelobrojni tip (int) kako bi se izbjegle pogreške pri spajanju (merge) dva velika seta podataka.
