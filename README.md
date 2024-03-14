# ING301 Prosjekt Del B: Persistens og database

## Formål

I det neste steget av prosjektet skal vi sørge for at den informasjonen som representeres i
et objektstruktur lagres permanent på en hard-disk slik at vi ikke mister noe
informasjonen når programmet avsluttes.

For å gjøre dette skal vi bruke et lettvekt databasesystem: [SQLite](https://www.sqlite.org/index.html), som 
er også [innebygget i Python sitt standard bibliotek](https://docs.python.org/3/library/sqlite3.html).

Applikasjonen fra del A skal utvides slik at
- den kan leser byggningsstrukturen og enhetsinformasjoner fra databasen,
- tilstanden til aktuatorer lagres persistent i databasen og
- man kan kjøre noen statistiske analyser og spørringer på sensormålinger.

## Setup

**Viktig Info:** Denne oppgaven bygger umiddelbart på Del A og det forventes at filene fra denne repository'en 
kopieres inn i et prosjekt der steg A er ferdig implementert. 
Du har to muligheter her:

1. Enten du bygger ummiddelbart videre på ditt eksisterende prosjekt.
2. Eller du begynner med et "fersk" prosjekt basert på vår løsningsforlag (du finner det på Canvas)


Vi antar at deres prosjekt repository ser noenlunne slik ut akkurat nå (eventuelt har dere ha laget flere Python moduler enn oss her):
```
.
├── README.md
├── smarthouse
│  ├── __init__.py
│  └── domain.py
└── tests
   ├── __init__.py
   ├── demo_house.py
   └── test_part_a.py
```

Dere skal nå kopiere de tre filene som befinner seg i denne repository'en inn i deres prosjekt.
Den enkleste måtem å gjøre det på er slik: Trykk på `Code` (grønne knappen) også velger dere `Download ZIP`.
Det nedlastede arkivet pakkes ut i roten av deres prosjektrepo, slik at de nye filene havner på rett plass.
Den resulterende mappestrukturen må se slik ut:

```
.
├── data
│  └── db.sql                   <-- nytt
├── README.md
├── smarthouse
│  ├── __init__.py
│  ├── domain.py
│  └── persistence.py           <-- nytt
└── tests
   ├── __init__.py
   ├── demo_house.py
   ├── test_part_a.py
   └── test_part_b.py           <-- nytt
```
Hvis dere har oppdatert inneholdet i `README.md`, pass på at dere ikker overskrive deres endringer!
Hvis dere har laget filer med samme navn som dem som er gitt her, så må dere skifte navn på deres egne file først for at 
alt fungerer (men det burde være lite sannsynlighet for det).

En liten forklaring på hva de tre nye filene gjør:
- `data/db.sqlite` SQLite database filen som inneholder et ferdig datasett dere skal jobbe videres med
- `smarthouse/persistence.py` inneholder et enkelt database grensesnitt klasse (`SmartHouseRepository`). Denne inneholder en del metoder som dere skal implementere.
- `tests/test_part_b.py` inneholder tester som dere kan bruke for å sjekke om alt har blitt utviklet og fungerer.

Når dere gå inn og åpne `smarthouse/persistence.py` så finner dere 5 metoder dere skal implementere: 

1. `load_smarthouse_deep()` (svarer til testene `test_basic_no_of_rooms()`, `test_basic_get_area_size()` og `test_basic_get_no_of_devices()`)
2. `get_latest_reading()` (svarer til testen `test_basic_read_values()`)
3. `update_actuator_state()` (svarer til testen `test_intermediate_save_actuator_state()`)
4. `calc_avg_temperatures_in_room()` (svarer til testen `test_zadvanced_test_humidity_hours()`)
5. `calc_hours_with_humidity_above()` (svarer til testen `test_zadvanced_test_temp_avgs()`)

Hver metode har en kommentar som beskriver hva som skal gjøres.
Den beste måten å komme i gang med denne oppgaven er å begynne med å _utforske_ den gitte databasen (`data/db.sqlite`).

## Utforsk tabellen

Oppgaven deres er nå til å få alle testene å bli grønn.
Før dere begynner med koding da, kan det være lurt å utforske databasen litt i forkant.
Dere kan bruke et verktøy som [DBeaver](https://dbeaver.io/) til dette.

Når dere åpner DBeaver for første gang skal dere til venstre se et vindu som heter `Database Navigator`.
Den ligner litt på filtre "explorer".

**TIPPS**: Hvis man har rotet seg bort å forskyvet vinduene hit og dit kan man komme seg tilbake til
utgangspunktet ved å trykke på `Window` (i vindu menyen) -> `Reset Perspective`.


Gjør så en høyreklikk i `Database Navigator` og  `Create` > `Connection` i kontekstmenyen.
I det nye vinduet som kommer opp, velg `SQLite` og så `Next`.
Cursoren skulle stå i et felt som heter `Path`.
Her skal vi skrive inn filstien til `db.sqlite` filen.

For å finne filstien kan dere
- Hvis dere bruker PyCharm: I Project-Explorer ved å høyreklikke på filen og så `Copy Path / Reference` -> `Absolute Path`.
- I VS Code: Skrive `pwd` i terminalvinduet, kopiere inn den stien som blir gitt ut som resultat og setter `db.sqlite` på slutten.

Nå kan dere lime inn den stien vi nettopp hadde kopiert i DBeaver vinduet.
Hvis dere trykker på `Connection details (type, name, ...)` knappen åpnes et nytt vindu da dere kan
gi et mer dekkende navn til forbindelsen, f.eks `ING301ProjectB`.
Dere avslutte med å trykke på `Finish`.

Den nye forbindelsen dykker nå opp i `Database Navigator`.
Gør en dobbelklikk på den.
Nå skulle dere se en aktiv (dvs. den har et grønt sjekkmerke) forbindelse mot prosjektets `db.sqlite` fil.
Når dere gjør en høyreklikk på den kan dere velge `SQL Editor` > `Open SQL Script` i kontekstmenyen.
Nå velger dere `New Script` slik at et nytt editorvindu åpner seg der dere kan skrive SQL.
F.eks kunne dere skrive 
```sql
SELECT name FROM sqlite_schema WHERE type = 'table';
```
for å finne ut hva tabeller det finnes og hva de heter.

Når vi vet hvordan tabellene heter, kan dere kjøre en `SELECT` mot dem:
```sql
SELECT * FROM  rooms;
```
vil gi der romstrukturen av det demohuset dere kjenner fra første delen.

## Mål og hvordan begynner jeg

Målet er som sagt å få alle testene grønt.
Testene kan deles inn i tre grupper:

### `test_basic_...`

Her må dere skrive enkle SQL `SELECT` spørringer i `load_smarthouse_deep()` og `get_latest_reading()` ved å bruke `cursor()`
metoden i `SmartHouseRepository` klassen. Dere kan [ta en titt i Python dokumentasjon av `sqlite3` modulen](https://docs.python.org/3/library/sqlite3.html)
for å sjekke hvordan skriver SQL i Python og håndterer resultatene.

### `test_intermediate_...`

Her må dere implementere funksjonalitet for at forandringer i objektene (aktuatorer) skal lagres varig i databasen.
For å realisere dette må dere kanskje utvide database strukturen: Kanskje legge til tabeller med `CREATE TABLE` eller
legge til en kolonne til en eksisterende tabell med `ALTER TABLE`.
Etterpå må kanskje legges til noe data som oppretter koblinger mot de eksisterende radene ved å bruke `INSERT` før 
dere til slutt kan bruke `UPDATE` for oppdatere radene i tabellen. 
Husk å kalle `commit()` på `Connection` objektet for at endrinene blir med!

### `test_advanced_...`

De resterende testene svarer til "statistikk"-funksjonen i `SmartHouseRepository`.
Konkret må dere skrive et tilsvarende `SELECT` spørring.
Disse kan anses som "litt av en nøtt" men bare prøv å se hvor langt dere kommer.
Følgende referanser kunne eventuelt være nyttig å bruke:


- https://www.sqlite.org/lang_datefunc.html
- https://www.w3resource.com/sql/subqueries/understanding-sql-subqueries.php
- https://www.w3schools.com/sql/sql_having.asp

Det kan være greit å utvikle i DBeaver først før dere legger det inn i et `cursor.execute("...")`

Lykke til!



