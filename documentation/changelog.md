# Changelog

## Viikko 3

- Käyttäjä voi klikata haitarinavigaatiota ja painamalla load nappia saada pylväskuvaajan reaaliaikaisista Applen osakkeiden hinnoista viimeisten 15 minuutin aikana, jolloin pörssi on ollut auki (-5 UTC aika-ikkuna).. 
- Käyttäjä saa myös load napista dataa Applen, Microsoftin ja Googlen osakkeiden hinnoista viimeisten 15 minuutin ajalta, jolloin pörssi on ollut auki (-5 UTC aika-ikkuna). 
- Lisätty Finance_machine-luokka, joka vastaa reaaliaikaisen datan saamisesta osakemarkkinoilta.
- Tehty hyvin alkeellinen käyttöliittymä src/main.py tiedostoon, jossa MainWindow luokka, joka vastaa käyttöliittymästä ja datan lataamisesta
- Tehty Mainwindow-luokkaan methodi, joka päivittää käyttäjän dashboard alueen osaan dataa osakkeiden hinnoista viimeisten 15 minuutin kauppojen ajalta.
- Testattu sovelluksen datan tarkkuuta, ja todettu olevan oikeassa.


## Viikko 4

- Käyttäjä voi nyt nähdä myös analyysi tietoja yrityksistä sekä yrityksen osakkeen hinnan painamalla analyze nappia.
- Käyttäjä voi lisätä uusia vertailtavia yrityksiä kirjoittamalla yrityksen osakkeen nimi osakenimenä esim. "NVDA".
- Käyttäjä näkee päivitetyn osakehinta vertailu kaavion painamalla analyze nappia.
- Tehty rakennemuutoksia koodiin, siten että se olisi skaalautuvampi eriyttämällä mm. datan hakeminen, analysointi + käsittelyä omiksi moduuleiksi
- Yhdistetty lataustoiminnallisuuden näkyvyys käyttäjän käyttöliittymänäkymään.
- Tehty testejä stock.py tiedostolle
- Pylint otettu käyttöön
  

## Viikko 5

- Käyttäjä voi nyt saada Williams R analyysia analysoitavista osakkeista, jossa tunnistetaan osakkeiden ylimyyntisyyttä ja yliostettavuutta.
- Kasvatettu koodin testikattavuutta
- Yhdistetty Williams R laskenta käyttöliittymään
- Lintattu koodia

## Viikko 6

- Käyttäjä voi nyt saada Moving Averages analyysia analysoitavista osakkeista, jossa seurataan osakkeiden keskihinnan vaihtelua.
- Kasvatettu koodin testikattavuutta
- Yhdistetty "Simple Moving Averages" laskenta käyttöliittymään
- Lintattu koodia


