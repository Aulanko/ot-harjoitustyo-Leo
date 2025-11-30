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


### Williams R laskenta ominaisuus. Socellus laskee indikaattorin osakkeiden yliostetuuden ja ylimyytyneisyyden tunnistamiseksi:
sequenceDiagram
    participant Käyttöliittymä
    participant StockAnalysis
    participant StockRepository
    participant YahooFinance

    Käyttöliittymä->>StockAnalysis: laske_yliostettu_ja_ylimyyty(symbol)
    StockAnalysis->>StockRepository: hae_historiset_tiedot(symbol, "1kk", "1pv")
    StockRepository->>YahooFinance: hae historialliset tiedot
    YahooFinance-->>StockRepository: hintadata
    StockRepository-->>StockAnalysis: DataFrame
    StockAnalysis->>StockAnalysis: laske Williams %R
    StockAnalysis-->>Käyttöliittymä: williams_r arvo
