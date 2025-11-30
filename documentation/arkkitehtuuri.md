```mermaid
flowchart TD
    A[Käyttöliittymä\nPyQt6] --> B[Toimintalogiikka\nStockAnalysis]
    B --> C[Datakerros\nStockRepository]
    C --> D[Ulkoiset rajapinnat\nYahoo Finance]
    
    C --> E[Välimuisti\nRedis]
    C --> F[Tietokanta\nSQLite]
    
    G[Datamallit\nStockData, StockSummary] -.-> B
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
