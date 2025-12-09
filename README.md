

# Ohjelmistotekniikka, harjoitustyö

## Tämä repositorio on kurssia : "Aineopintojen harjoitustyö: Ohjelmistotekniikka (4 op)" varten

Tässä on normaalia tekstiä  **boldattuna** ja tässä tekstiä *kursivoituna* 



### [Käyttöohje](./documentation/kayttoohje.md)

### [Vaatimusmäärittely](./documentation/vaatimusmaarittely.md)

### [Arkkitehtuurikuvaus](./documentation/arkkitehtuuri.md)

### [Tuntikirjanpito](./documentation/tuntikirjanpito.md)

### [Changelog](./documentation/changelog.md)


# Osake applikaatio. 
#### Tämä applikaatio hakee verkosta live osakedataa ja tekee niistä analyyseja sekä hinta vertailua. Käyttäjä voi hakea haluamastaan osakkeestaan hinta-dataa

### Asenna riippuvuudet komennolla:
(sitä ennen varmista, että poetry on ladattuna ja python version on >=3.11)

```
poetry install
```

### Käynnistä sovellus komennolla:
(huom, jos käynnistää ensimmäistä kertaa, niin voi kestää pieni tovi, että ohjelma käynnistyy, sama pätee kun painaa analyze nappia)
```
poetry run invoke start
```

### Aja Pytestit:
```
poetry run invoke test
```

### Coverage-raportti
```
poetry run invoke coverage_report
```

### Linttaus

```
poetry run invoke lint
```

### Koodin linttauksen formatointia
```
poetry run invoke format_for_lint
```
