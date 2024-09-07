import unittest
import numpy as np
from Traffic_Collision_Avoidance import acceleration

class TestAcceleration(unittest.TestCase):

    # für unterschiedliche Vektoren
    def test_values(self):
        np.testing.assert_array_equal(acceleration(np.array([2, 3.5]), 4), np.array([0.0625, -0.125]))
        np.testing.assert_array_equal(acceleration(np.array([-1, 0.5]), 2.5), np.array([1.12, 0.64]))
        np.testing.assert_array_almost_equal(acceleration(np.array([5, -7.2]), 3), np.array([-0.5556, 2.1556]), decimal=3)
        np.testing.assert_array_almost_equal(acceleration(np.array([100, -150]), 50), np.array([-0.078, 0.122]), decimal=3)
        np.testing.assert_array_almost_equal(acceleration(np.array([0.031, 0.058]), 0.047), np.array([2235.40, 2210.955]), decimal=3)

    # falsche Datentypen
    def test_type(self):
        self.assertRaises(TypeError, acceleration, True, [1, 1])
        self.assertRaises(TypeError, acceleration, "35", [1, 1])
        self.assertRaises(TypeError, acceleration, 5, [1, 1])
        self.assertRaises(ValueError, acceleration, [1, 2, 3], [1, 1])