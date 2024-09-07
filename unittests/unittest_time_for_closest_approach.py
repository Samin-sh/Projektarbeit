import unittest
import numpy as np
from Traffic_Collision_Avoidance import t_ca

class TestT_CA(unittest.TestCase):

    # beträge testen
    def test_values(self):
        self.assertAlmostEqual(t_ca([5, 8], [3, 2]), -2.3846, places = 4)
        self.assertAlmostEqual(t_ca([-4, 6], [-5, -7]), 0.2973, places= 4)
        self.assertEqual(t_ca([3, 7], [0, 0]), 1e9)
        self.assertEqual(t_ca([-3, -9], [-2, -6]), -1.5)
        self.assertAlmostEqual(t_ca([-2563, 4321], [3821, -6431]), 0.6716, places = 4)
        self.assertAlmostEqual(t_ca([0.0032, 0.0012], [0.0048, -0.0065]), -0.1158, places = 4)

    # datentypen testen
    def test_type(self):
        self.assertRaises(ValueError, t_ca, [5, 7, 2], [3, 2])
        self.assertRaises(TypeError, t_ca, "test", [3, 2])
        self.assertRaises(TypeError, t_ca, 32, [3, 2])
        self.assertRaises(TypeError, t_ca, None, [3, 2])



