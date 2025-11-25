

# Ohjelmistotekniikka, harjoitustyö

## Tämä repositorio on kurssia : "Aineopintojen harjoitustyö: Ohjelmistotekniikka (4 op)" varten

Tässä on normaalia tekstiä  **boldattuna** ja tässä tekstiä *kursivoituna* 



### [Käyttöohje](./harjoitustyo/README.md)

### [Vaatimusmäärittely](./documentation/vaatimusmaarittely.md)

### [Tuntikirjanpito](./documentation/tuntikirjanpito.md)

### [Changelog](./documentation/changelog.md)

flowchart TD
    
    B --> C[Asenna riippuvuudet komennolla:]
    C --> D["poetry install"]

    F --> G[Käynnistä sovellus komennolla:]
    G --> H["poetry run invoke start"]

