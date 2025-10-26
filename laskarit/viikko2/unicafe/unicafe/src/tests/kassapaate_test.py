import unittest 
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.kortti = Maksukortti(10000)

    def test_luodun_kassapäätteen_rahamäärä_ja_myytyjen_lounaiden_määrä_on_oikea(self):
        self.assertEqual(100000, self.kassapaate.kassassa_rahaa)
        self.assertEqual(0, self.kassapaate.edulliset)
        self.assertEqual(0, self.kassapaate.maukkaat)

    def test_käteisosto_toimii_sekä_edullisten_että_maukkaiden_lounaiden_osalta(self):
        self.kassapaate.syo_edullisesti_kateisella(500)
        self.assertEqual(100240, self.kassapaate.kassassa_rahaa)
        self.kassapaate.syo_maukkaasti_kateisella(500)
        self.assertEqual(100640, self.kassapaate.kassassa_rahaa)

        self.assertEqual(self.kassapaate.edulliset, 1)
        self.assertEqual(self.kassapaate.maukkaat, 1)

        vaihtoraha_edullinen = self.kassapaate.syo_edullisesti_kateisella(500)
        vaihtoraha_maukas = self.kassapaate.syo_maukkaasti_kateisella(500)
        self.assertEqual(260,vaihtoraha_edullinen)
        self.assertEqual(100, vaihtoraha_maukas)

        #Tässä kohtaa aikaisemmin (ylhäällä oleva koodi, ostettiin uudestaan kasaan)

        self.kassapaate.syo_edullisesti_kateisella(50)
        self.assertEqual(101280, self.kassapaate.kassassa_rahaa)
        self.assertEqual(self.kassapaate.edulliset,2)
        liian_vahan_rahaa_edullinen = self.kassapaate.syo_edullisesti_kateisella(50)
        self.assertEqual(50, liian_vahan_rahaa_edullinen)

        self.kassapaate.syo_maukkaasti_kateisella(300)
        self.assertEqual(101280, self.kassapaate.kassassa_rahaa)
        self.assertEqual(self.kassapaate.maukkaat, 2)
        liian_vahan_rahaa_maukas = self.kassapaate.syo_maukkaasti_kateisella(300)
        self.assertEqual(300, liian_vahan_rahaa_maukas)
        

    def test_korttiosto_toimii_sekä_edullisten_että_maukkaiden_lounaiden_osalta(self):
        self.kassapaate.syo_edullisesti_kortilla(self.kortti)
        self.assertEqual(9760, self.kortti.saldo)
        self.kassapaate.syo_maukkaasti_kortilla(self.kortti)
        self.assertEqual(9360, self.kortti.saldo)

        self.assertEqual(self.kassapaate.edulliset, 1)
        self.assertEqual(self.kassapaate.maukkaat, 1)

        

        self.kortti.ota_rahaa(self.kortti.saldo)
        riittikö_raha_edullinen = self.kassapaate.syo_edullisesti_kortilla(self.kortti)
        self.assertEqual(False, riittikö_raha_edullinen)
        self.assertEqual(self.kassapaate.edulliset,1)
        

        self.kassapaate.syo_maukkaasti_kortilla(self.kortti)
        riittikö_raha_maukas = self.kassapaate.syo_edullisesti_kortilla(self.kortti)
        self.assertEqual(False, riittikö_raha_maukas)
        self.assertEqual(self.kassapaate.maukkaat, 1)
        self.assertEqual(100000, self.kassapaate.kassassa_rahaa)

        self.kassapaate.lataa_rahaa_kortille(self.kortti,5000)
        self.assertEqual(self.kortti.saldo, 5000)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 105000)
           





        

    


