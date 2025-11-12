# Changelog

## Viikko 3

- Käyttäjä voi klikata haitarinavigaatiota ja painamalla load nappia saada pylväskuvaajan reaaliaikaisista Applen osakkeiden hinnoista viimeisten 15 minuutin aikana, jolloin pörssi on ollut auki (-5 UTC aika-ikkuna).. 
- Käyttäjä saa myös load napista dataa Applen, Microsoftin ja Googlen osakkeiden hinnoista viimeisten 15 minuutin ajalta, jolloin pörssi on ollut auki (-5 UTC aika-ikkuna). 
- Lisätty Finance_machine-luokka, joka vastaa reaaliaikaisen datan saamisesta osakemarkkinoilta.
- Tehty hyvin alkeellinen käyttöliittymä src/main.py tiedostoon, jossa MainWindow luokka, joka vastaa käyttöliittymästä ja datan lataamisesta
- Tehty Mainwindow-luokkaan methodi, joka päivittää käyttäjän dashboard alueen osaan dataa osakkeiden hinnoista viimeisten 15 minuutin kauppojen ajalta.
- Testattu sovelluksen datan tarkkuuta, ja todettu olevan oikeassa.




