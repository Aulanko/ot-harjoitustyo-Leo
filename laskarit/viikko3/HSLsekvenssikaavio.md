

```mermaid
sequenceDiagram
    participant main
    participant laitehallinto
    participant rautatientori
    participant ratikka6
    participant bussi244
    

    main->> laitehallinto: laitehallinto = HKLLaitehallinto()
    main->> rautatientori: rautatietori = Lataajalaite()
    main->> ratikka6: ratikka6 = Lukijalaite()
    main->> bussi244: bussi244 = Lukijalaite()

    laitehallinto ->> rautatientori: laitehallinto.lisaa_lataaja(rautatietori)
    laitehallinto->>ratikka6:laitehallinto.lisaa_lukija(ratikka6)
    laitehallinto ->>bussi244: laitehallinto.lisaa_lukija(bussi244)

    participant lippuluukku
    main->>lippuluukku: lippu_luukku = Kioski()
    participant Kallenkortti
    lippuluukku->>Kallenkortti:kallen_kortti = lippu_luukku.osta_matkakortti("Kalle")
    rautatientori->>Kallenkortti: rautatietori.lataa_arvoa(kallen_kortti, 3)
    ratikka6->>Kallenkortti: ratikka6.osta_lippu(kallen_kortti, 0)
    bussi244->>Kallenkortti: bussi244.osta_lippu(kallen_kortti, 2)
    
