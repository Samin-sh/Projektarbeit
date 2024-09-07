import unittest
import numpy as np
from Traffic_Collision_Avoidance import r_ca

class TestR_CA(unittest.TestCase):

    # für unterschiedliche Vektoren
    def test_values(self):
        np.testing.assert_array_equal(r_ca(np.array([-2, 5]), np.array([-2, 5])), np.array([-3, 4]))
        np.testing.assert_array_equal(r_ca(np.array([1, 4]), np.array([6, 8])), np.array([0.62, 3.62]))
        np.testing.assert_array_almost_equal(r_ca(np.array([55, 3]), np.array([17, 86])), np.array([54.844, 2.844]), decimal = 3)
        np.testing.assert_array_equal(r_ca(np.array([-7, -3]), np.array([-9, -12])), np.array([-7.44, -3.44]))
        np.testing.assert_array_almost_equal(r_ca(np.array([-742, 534]), np.array([632, -229])), np.array([-740.691, 535.310]), decimal = 2)
        np.testing.assert_array_equal(r_ca(np.array([-7, 4]), np.array([0, 0])), np.array([-7 - 1e9, 4 - 1e9]))

    # für Kommazahlen
    def test_floats(self):
        np.testing.assert_array_almost_equal(r_ca(np.array([2.6, 8.5]), np.array([5.7, 13.9])), np.array([2.0108, 7.918]),
                                             decimal=2)
        np.testing.assert_array_almost_equal(r_ca(np.array([253.42, 638.11]), np.array([492.23, 671.97])),
                                             np.array([252.6222, 637.3122]), decimal=4)

    # falsche Datentypen
    def test_type(self):
        self.assertRaises(TypeError, r_ca, True, [1, 1])
        self.assertRaises(TypeError, r_ca, "35", [1, 1])
        self.assertRaises(TypeError, r_ca, 5, [1, 1])
        self.assertRaises(ValueError, r_ca, [1, 2, 3], [1, 1])
