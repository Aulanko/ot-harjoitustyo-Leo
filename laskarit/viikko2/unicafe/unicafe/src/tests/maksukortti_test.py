import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_kortin_salo_alussa_oikein(self):
        self.assertEqual(str(self.maksukortti),"Kortilla on rahaa 10.00 euroa",)

    def test_rahan_lataaminen_kasvattaa_saldoa_oikein(self):
        self.maksukortti.lataa_rahaa(30)
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.30 euroa")

    def test_rahan_ottaminen_toimii(self):
        self.maksukortti.ota_rahaa(500)
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 5.00 euroa")
        self.maksukortti.ota_rahaa(9999)
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 5.00 euroa")
        onnistuu = self.maksukortti.ota_rahaa(20)
        self.assertEqual(True, onnistuu)

        

