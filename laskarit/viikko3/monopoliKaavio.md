
## Monopoli, alustava luokkakaavio

```mermaid
 classDiagram
    Monopolipeli "1" -- "2" Noppa
    Monopolipeli "1" -- "1" Pelilauta
    Pelilauta "1" -- "40" Ruutu
    Ruutu "1" -- "1" Ruutu : seuraava
    Ruutu "1" -- "1" Aloitusruutu
    Ruutu "1" -- "11" Vankila
    Ruutu "1" -- "6, 23,37" Sattuma/Yhteismaa
    Ruutu "1" -- "6,16,26,36, 13, 28" Asemat/laitokset



    Ruutu "1" -- "0..8" Pelinappula
    Pelinappula "1" -- "1" Pelaaja
    Pelaaja "2..8" -- "1" Monopolipeli
```
