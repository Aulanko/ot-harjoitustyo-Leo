

# Ohjelmistotekniikka, harjoitustyö

## Tämä repositorio on kurssia : "Aineopintojen harjoitustyö: Ohjelmistotekniikka (4 op)" varten

Tässä on normaalia tekstiä  **boldattuna** ja tässä tekstiä *kursivoituna* 



### [Käyttöohje](./harjoitustyo/README.md)

### [Vaatimusmäärittely](./documentation/vaatimusmaarittely.md)

### [Tuntikirjanpito](./documentation/tuntikirjanpito.md)

### [Changelog](./documentation/changelog.md)



### Asenna riippuvuudet komennolla:

```
poetry install
```

### Käynnistä sovellus komennolla:

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
