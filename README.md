# ING301 prosjekt - Del C

I del C av prosjektet skal dere implementere en REST API for en smarthus sky-tjeneste ved bruk av rammeverket [FastAPI](https://fastapi.tiangolo.com).

## Setup og Startup

Start-koden for prosjektet finnes i dette GitHub repository: 

<https://github.com/selabhvl/ing301-projectpartC-startcode.git>

Igjen forutsettes at dere har implementert en fullstendig løsning til forrige oppgaven (del B).
Enten kan dere bygge direkte på deres eksisterende løsning eller dere begynner med et helt fersk
repository ved å klone [startkoden](https://github.com/selabhvl/ing301-projectpartA-startcode) for første delen
igjen også kopiere filene til henholdsvis løsningsforslagene A og B inn for å ha et utgangspunkt til denne oppgaven.

Dere kopierer inn filene fra dette repository'et ("Download as ZIP") inn i det eksisterende prosjekt slik at 
mappestrukturen skal se noenlunde slik ut:

```
.
├── data
│  └── db.sql
├── README.md               <-- erstatt hvis du vil
├── smarthouse
│  ├── __init__.py
│  ├── api.py               <-- nytt
│  ├── domain.py
│  └── persistence.py
├── tests
│  ├── __init__.py
│  ├── bruno                <-- nytt
│  │  └── ...
│  ├── demo_house.py
│  ├── test_part_a.py
│  └── test_part_b.py
└── www                     <-- nytt
   └── ...
```


Selv om det er mulig (og at dette vil være en veldig lærrik oppgave) å implementere en HTTP-server helt fra bunn av,
så ville dette være veldig tidkrevende også. Vi skal derfor bruke en bibliotek som heter [FastAPI](https://fastapi.tiangolo.com).
FastAPI er ikke en del Python sin standard bibliotek og må derfor installeres som en [Python Packages](https://packaging.python.org/en/latest/overview/).
Installasjon av packages kan være en utfordring siden man må manøvrere ting som [Externally Managed Environments](https://packaging.python.org/en/latest/specifications/externally-managed-environments/#externally-managed-environments), "package managers" som [`pip`](), [`conda`](), [`poetry`]() osv...
Dette kan være utfordrende i starten!

En god praksis er å lage noe som kalles en [virtual environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment) for  hver Python prosjekt. 
Dette gjør at man kan styre hvilken Python-fortolker som skal brukes og for å kunne holde paketer adskilt. 

For å oprette en slik virtual environment åpner du et nytt terminalvindu og så beveger du deg inn i prosjektmappen.
Her utfører du følgende kommando:
```powershell
py -m venv .venv
```
hvis du bruker Windows, eller
```shell
python3 -m venv .venv
```
hvis du bruker Linux/UNIX/MacOS.

Vær også obs på at under noen operativsystemer må `venv`-modulen installeres for første gang gjennom operativsystemets pakkeforvaltning, f.eks.
under Ubuntu må du utføre:
```shell
sudo apt-get install python3-venv
```

Etter at det virtuelle Python miljøet er blitt opprettet må det aktiveres med
```powershell 
.venv\Scripts\activate
```
under Windows, eller 
```shell
source .venv/bin/activate
```
under Linux/UNIX/MacOS.


Du vil nå se at ledeteksten i konsollen har forandret seg litt og hvis du nå sjekker hvilke `python` og `pip` er som aktive:

Windows:
```powershell
where python 
where pip
```

Linux/UNIX/MacOS
```shell
which python 
which pip
```

Da vil du se at disse nå peker mot den `.venv`-mappen som ble opprettet før.

Nå at det virtuelle Python miljø er på plass er det lurt å sjekke om `pip` der og oppdatert:
```shell
python -m pip install --upgrade pip
```
Istedenfor `python -m pip` burde du også kunne skrive bare `pip`.
Hvis du får en feilmelding at modulen `pip` kan ikke finnes så må du eventuelt sjekke om denne pakken må installeres 
gjennom operativsystemets forvaltningssystem (noe som heter `python3-pip`).

Når `pip` er på plass kan _FastAPI_ samt avhengigheter installeres ved å kjøre følgende kommandoer:
```
python -m pip install fastapi 
python -m pip install "uvicorn[standard]"
```

Nå skulle alt være på plass for å kunne kjøre applikasjonen:

```shell
python -m uvicorn smarthouse.api:app --reload
```

når konsollen viser noe slik:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [28720]
INFO:     Started server process [28722]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```
så er web applikasjonen klart! Du kan åpner nettleseren på 

> <http://127.0.0.1:8000>

for å se en liten demoside og 

> <http://127.0.0.1:8000/docs>

vil gi deg en oversikt over REST ressursene som finnes.

Hvis du ikke allerede har gjort det, så er det nå en god tidspunkt å laste ned [Bruno](https://www.usebruno.com/), 
starte det, lage en ny "collection" og prøve å sende en HTTP GET request til `http:127.0.0.1:8000/hello`.

Gratulerer! Da er Setup avsluttet og du er klar til å begynne med oppgaven!

## Noen ord vedrørende virtuelle Python miljø

Enn så lenge du holder konsollen åpen så vil være web-tjeneren være aktivt.
I tillegg vil den automatisk reagere på alle endringer i koden og automatisk oppdatere seg slik
at du får en nesten sømløs opplevelse.
Når du vil likevel avslutte applikasjonen må du sette fokus på terminalvinduet også trykker du <kbd>Ctrl</kbd> + <kbd>C</kbd>
samtidig, da kommer du tilbake til ledeteksten.

Hvis du vil gå ut av det virtuelle Python miljøet (f.eks. for å jobbe med et annen Python projsket) kan du kalle:
```shell
deactivate
```

For å komme inn i det virtuelle miljøet igjen gjør du akkurat likt som beskrevet ovenfor ved å kalle `activate`.
Husk at dette også må gjøres når du starter PCen din på nytt eller du åpner et nytt terminalvindu.

I tillegg vil du kanskje også at din editor eller IDE samarbeider med det virtuelle miljøet. 
Sjekk dokumentasjonen til [VS Code](https://code.visualstudio.com/docs/python/environments) eller [PyCharm](https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html).
I de fleste tilfellene vil disse automatisk oppdager at det finnes en `venv` i ditt prosjekt og forholder seg tilsvarende.

## Oppgavebeskrivelse

Som nevnt består altså oppgaven i det å lage en REST API for smarthuset. 
Konkret skal dere opprette følgende endepunkter:

Det skal finnes endepunkter får inspisere strukturen til huset:

- `GET smarthouse/` - information on the smart house
- `GET smarthouse/floor` - information on all floors
- `GET smarthouse/floor/{fid}` - information about a floor given by `fid` 
- `GET smarthouse/floor/{fid}/room` - information about all rooms on a given floor `fid`
- `GET smarthouse/floor/{fid}/room/{rid}`- information about a specific room `rid` on a given floor `fid`

Det skal finnes endepunkter for tilgang til enheter:

- `GET smarthouse/device` - information on all devices
- `GET smarthouse/device/{uuid}` - information for a given device identfied by `uuid`

Det skal finnes spesielle endepunkter for tilgang til sensor funksjoner:

- `GET smarthouse/sensor/{uuid}/current` - get current sensor measurement for sensor `uuid`
- `POST smarthouse/sensor/{uuid}/current` - add measurement for sensor `uuid`
- `GET smarthouse/sensor/{uuid}/values?limit=n` - get `n` latest available measurements for sensor `uuid`. If query parameter not present, then all available measurements.
- `DELETE smarthouse/sensor/{uuid}/oldest` - delete oldest measurements for sensor `uuid`

Det skal finnes spesielle endepunkter for tilgang til aktuator funskjoner:

- `GET smarthouse/actuator/{uuid}/current` - get current state for actuator `uuid`
- `PUT smarthouse/device/{uuid}` - update current state for actuator `uuid`

For de fleste av endepunktenes funksjonalitet kan en mye av funksjonene i `SmartHouse`-klassen sannsynligvis gjenbrukes. 
For noen må kanskje nytt funksjonalitet utvikles (husk også database tilkoblingen).
Husk også at data som returneres fra endepunktet eller sendes til endepunktet skal være i [JSON](https://www.json.org/json-en.html)-formatet.
FastAPI er i stand til å automatisk overføre Python objekter til JSON i noen tilfelle:

- strenger (`str`),
- tall (`int`, `float`),
- sannhetsverdier (`bool`),
- `None`-verdien,
- lister og ordbøker med streng-nøkler som igjen inneholder lister, ordbøker eller verdiene nevnt ovenfor.

Alternativt kan du også bruke [Pydantic](https://docs.pydantic.dev/latest/)-biblioteket (den kommer automatisk med når man installerer FastAPI)
for å [oversette dine egne klasser automatisk](https://docs.pydantic.dev/latest/concepts/models/).

Viktig er at dere på forhånd tar en avgjørelse om hvordan inn- og utdata for hver endepunkt skal være strukturert. 


## Testing 

En del av oppgaven er å teste deres endepunkter. 
For dette anbefaler vi Bruno-verktøyet som gjør det mulig å lage en _Collection_ av test-request og sjekker disse inn i git.
Dette startkode repository inneholder en slik påbegynt "Test-Suite" som ligger under `tests/bruno`.
Du kan åpne denne samlingen ved å trykke "Open Collection" når du starter Bruno og så navigerer du den nevnte mappen i din filsystem. 
Her er det også demonstrert hvordan du kan bruker _variable_ og hvordan man skrive tests i Bruno ved brul av _assertions_ (forventninger).

## Tips og diverse

For å løse oppgaven kan det være en god idé å søke inspirasjon i eksemplet fra forelesningen i uke 12 der FastAPI ble brukt til å utvikle en REST API for sykkelcomputer eksemplet:

Koden finnes her:

> <https://github.com/selabhvl/ing301public/tree/main/examples/12_restapi_webservices>

Der er også hjelp å hente i dokumentasjonen for FastAPI som finnes via:

> <https://fastapi.tiangolo.com>

