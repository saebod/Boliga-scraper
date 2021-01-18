# Boliga-scraper

Boliga-scraper gøre det muligt at indhente data omhandlede solgte boliger fra boliga.dk 

## Usage

```python
From BoligaScraper import GetBoligainfo

GetBoligainfo(zipfrom=1000,zipto=1100,property=3,salestype=1,yearfrom=2019, yearto=2020)
```
BoligScraper tager følgende argumenter

| Argument|Beskrivelse  |
|--|--|
|zipfrom|start interval for postnummeret den skal scrape|
 |zipto|slut interval for postnumeret den skal scrape, hvis zipto er tom scraper den kun postnummeret der er angiver i zipfrom| 
 |property|Angiver boligtype som kan være følgende: 1: Villa, 2: Rækkehus, 3: Ejerlejlighed, 4: Fritidshus, 5: Landejendom|
 |salestype| Angiver handelstype som kan være følgende: 1: Almindelig frihandel 2: Familieoverdragvelse 3: Auktion 4: Øvrigt|
 |yearfrom|Angiver start intervallet for salgsåret
  |yearto|Angiver slut intervallet for salgsåret, hvis dette felt er tomt vil salgsåret kun være yearfrom

Output er en dataframe med følgende oplysninger
| Navn |Beskrivelse  |
|--|--|
|Adresse | Adresse inklusiv postnummer og by  |
|Boligpris|Angiver Salgsprisen for ejendommen  |
|Salgsdato|Angiver datoen for hvornår ejendommen er solgt  |
|kvm|Angiver kvadratmeter for boligen|
|Rooms|Angiver antal værelser|
|kvmpris| Angiver kvadratmeterprisen|
|byggeaar|Angiver byggeåret for ejendommen|
|boligtype| angivert hvilken type bolig det er(Villa, Rækkehus, Ejerlejlighed, Fritidshus, Landejendom)
## Bemærk
Bemærk at webscraping bliver gjort med selenium med google Chrome driver som automatisk hentes.

