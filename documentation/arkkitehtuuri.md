# Arkkitehtuurikuvaus

## Rakenne

```mermaid
flowchart TD
    A[Käyttöliittymä<br>PyQt6] --> B[Toimintalogiikka<br>StockAnalysis]
    B --> C[Datakerros<br>StockRepository]
    C --> D[Ulkoiset rajapinnat<br>Yahoo Finance]
    
    C --> E[Välimuisti<br>Redis]
    C --> F[Tietokanta<br>SQLite]
    
    G[Datamallit<br>StockData, StockSummary] -.-> B
    G -.-> C
    
    subgraph "Sovelluksen ydin"
        B
        G
    end
    
    subgraph "Infrastruktuuri"
        C
        E
        F
    end
 ```


### Williams R laskenta ominaisuus. Socellus laskee indikaattorin osakkeiden yliostetuuden ja ylimyytyneisyyden tunnistamiseksi:


```mermaid
sequenceDiagram
    participant Käyttöliittymä
    participant StockAnalysis
    participant StockRepository
    participant YahooFinance

    Käyttöliittymä->>StockAnalysis: laske yliostettu ja ylimyyty(symbolille)
    StockAnalysis->>StockRepository: hae historiset tiedot(osake nimi, kuinka pitkältä: "1kk", data pisteiden aikaväli: "1pv")
    StockRepository->>YahooFinance: hae historialliset tiedot
    YahooFinance-->>StockRepository: hintadata
    StockRepository-->>StockAnalysis: DataFrame
    StockAnalysis->>StockAnalysis: laske Williams %R
    StockAnalysis-->>Käyttöliittymä: williams r arvo

    Käyttöliittymä->>StockAnalysis: laske liikkuvat keskiarvot(symbolille)
    StockAnalysis->>StockRepository: hae historiset tiedot(osake nimi, kuinka kaukaa:"200pv", data pisteiden aikaväli="1pv")
    StockRepository->>YahooFinance: hae historialliset tiedot
    YahooFinance-->>StockRepository: hintadata
    StockRepository-->>StockAnalysis: DataFrame
    StockAnalysis->>StockAnalysis: laske 20,50 ja 200 päivän keskiarvot
    StockAnalysis-->>Käyttöliittymä: liikkuvat keskiarvot