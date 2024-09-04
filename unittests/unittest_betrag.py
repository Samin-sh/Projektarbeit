import unittest
from Traffic_Collision_Avoidance import betrag
class Testbetrag(unittest.TestCase):
    #beträge testen
    def test_values(self):
        self.assertEqual(betrag(3, 4), 5)
        self.assertEqual(betrag(6, 8), 10)
        self.assertEqual(betrag(15, 20), 25)
        self.assertEqual(betrag(3/5, 4/5), 1)
    #datentypen testen
    def test_type(self):
        self.assertRaises(TypeError, betrag, True)
        self.assertRaises(TypeError, betrag, "2")

    #negative Zahlen testen
    def test_negativ(self):
        self.assertEqual(betrag(-3, -4), -5)
        self.assertEqual(betrag(-6, -8), 10)
