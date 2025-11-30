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
