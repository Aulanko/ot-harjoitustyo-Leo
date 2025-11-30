```mermaid
flowchart TD
    A[Käyttöliittymä\nPyQt6] --> B[Toimintalogiikka\nStockAnalysis]
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
