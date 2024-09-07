import unittest
import numpy as np
from Traffic_Collision_Avoidance import delta

class TestDelta(unittest.TestCase):

    # falls die Vektoren identisch sind
    def test_same_values(self):
        np.testing.assert_array_equal(delta(np.array([3, 8]), np.array([3, 8])), np.array([0, 0]))
        np.testing.assert_array_equal(delta(np.array([-2, 5]), np.array([-2, 5])),np.array([0, 0]))
        np.testing.assert_array_equal(delta(np.array([-4, -1]), np.array([-4, -1])), np.array([0, 0]))

    # für ungleiche Vektoren
    def test_diff_values(self):
        np.testing.assert_array_equal(delta(np.array([1, 4]), np.array([6, 8])), np.array([-5, -4]))
        np.testing.assert_array_equal(delta(np.array([47, 5]), np.array([12, 69])), np.array([35, -64]))
        np.testing.assert_array_equal(delta(np.array([-5, -4]), np.array([-5, -4])), np.array([0, 0]))
        np.testing.assert_array_equal(delta(np.array([-365, 723]), np.array([945, -483])), np.array([-1310, 1206]))
        np.testing.assert_array_equal(delta(np.array([-2, 5]), np.array([0, 0])), np.array([-2, 5]))
    # für Kommazahlen
    def test_floats(self):
        np.testing.assert_array_almost_equal(delta(np.array([4.5, 7.4]), np.array([2.3, 5.5])), np.array([2.2, 1.9]), decimal=3)
        np.testing.assert_array_almost_equal(delta(np.array([125.42, 248.98]), np.array([378.32, 631.73])), np.array([-252.9, -382.75]), decimal=2)

    # falsche Datentypen
    def test_type(self):
        self.assertRaises(TypeError, delta, True, [1, 1])
        self.assertRaises(TypeError, delta, "35", [1, 1])
        self.assertRaises(TypeError, delta, 5, [1, 1])
        self.assertRaises(ValueError, delta, [1, 2, 3], [1, 1])
        self.assertRaises(TypeError, delta, None, [1, 1])