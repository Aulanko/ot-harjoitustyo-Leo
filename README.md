

# Ohjelmistotekniikka, harjoitustyö

## Tämä repositorio on kurssia : "Aineopintojen harjoitustyö: Ohjelmistotekniikka (4 op)" varten

Tässä on normaalia tekstiä  **boldattuna** ja tässä tekstiä *kursivoituna* 



### [Käyttöohje](./harjoitustyo/README.md)

### [Vaatimusmäärittely](./documentation/vaatimusmaarittely.md)

### [Tuntikirjanpito](./documentation/tuntikirjanpito.md)

### [Changelog](./documentation/changelog.md)


```mermaid
flowchart TD
    A[Asenna riippuvuudet] --> B["poetry install"]
    C[Käynnistä sovellus] --> D["poetry run invoke start"]
    
    E[Muut invoke-komennot] --> F["poetry run invoke test"]
    E --> G["poetry run invoke coverage_report"]
    E --> H["poetry run invoke lint"]
    E --> I["poetry run invoke format_for_lint"]

