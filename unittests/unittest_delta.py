import unittest
from Traffic_Collision_Avoidance import delta

class TestDelta(unittest.TestCase):
    #beträge testen
    #sind es immer int zahlen????
    def test_values(self):
        self.assertEqual(delta(5,3), 2)
        self.assertEqual(delta(5,0), 5)
        self.assertEqual(delta(10,1), 9)
        self.assertEqual(delta(345,175), 170)
        self.assertEqual(delta(3,5), -2)
        self.assertEqual(delta(5,4), 0)
        self.assertEqual(delta(2.8,3.5), -0.7)
        self.assertEqual(delta(9.3,2.5), 6.8)

    def test_type(self):
        self.assertRaises(TypeError, delta, True)
        self.assertRaises(TypeError, delta, "35")

        
