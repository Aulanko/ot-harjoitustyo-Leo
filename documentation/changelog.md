# Changelog

## Viikko 3

- Käyttäjä voi klikata haitarinavigaatiota ja painamalla load nappia saada pylväskuvaajan reaaliaikaisista Applen osakkeiden hinnoista viimeisten 15 minuutin aikana, jolloin pörssi on ollut auki (-5 UTC aika-ikkuna).. 
- Käyttäjä saa myös load napista dataa Applen, Microsoftin ja Googlen osakkeiden hinnoista viimeisten 15 minuutin ajalta, jolloin pörssi on ollut auki (-5 UTC aika-ikkuna). 
- Lisätty Finance_machine-luokka, joka vastaa reaaliaikaisen datan saamisesta osakemarkkinoilta.
- Tehty hyvin alkeellinen käyttöliittymä src/main.py tiedostoon, jossa MainWindow luokka, joka vastaa käyttöliittymästä ja datan lataamisesta
- Tehty Mainwindow-luokkaan methodi, joka päivittää käyttäjän dashboard alueen osaan dataa osakkeiden hinnoista viimeisten 15 minuutin kauppojen ajalta.
- Testattu sovelluksen datan tarkkuuta, ja todettu olevan oikeassa.


## Viikko 4

- Käyttäjä voi nyt nähdä myös analyysi tietoja yrityksistä, jotka ladattiin load-napista.
- Luotu Analyze-luokka, joka vastaa datan analysoinnista ja suuremmista matemaattisista operaatioista, joita tehdään datalle.
- Yhdistetty lataustoiminnallisuuden näkyvyys käyttäjän käyttöliittymänäkymään.
- Tehty testejä Analyze-luokalle.



