

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
    
