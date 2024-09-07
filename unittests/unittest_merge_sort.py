import unittest
from Traffic_Collision_Avoidance import merge_sort

def merge_sort(l):
    if len(l) > 1:
        half = len(l) // 2
        left_l = l[:half]
        right_l = l[half:]

        merge_sort(left_l)
        merge_sort(right_l)

        i = 0
        j = 0
        k = 0

        while i < len(left_l) and j < len(right_l):
            if left_l[i][0] < right_l[j][0]:
                l[k] = left_l[i]
                i += 1
            else:
                l[k] = right_l[j]
                j += 1
            k += 1

        while i < len(left_l):
                l[k] = left_l[i]
                k += 1
                i += 1

        while j < len(right_l):
                l[k] = right_l[j]
                k += 1
                j += 1
class TestMergeSort(unittest.TestCase):

    # testet Listen mit nur positive Zahlen
    def test_positive_values(self):

        l1 = [(4, "puck"), (3, "puck"), (7, "puck"), (2, "puck"), (9, "puck"), (4, "puck"),
                                     (1, "puck"), (0, "puck"), (6,"puck"), (3, "puck")]
        merge_sort(l1)
        sorted_1 = [(0, "puck"), (1, "puck"), (2, "puck"), (3, "puck"), (3, "puck"), (4, "puck"),
                                     (4, "puck"), (6, "puck"), (7,"puck"), (9, "puck")]
        self.assertEqual(l1, sorted_1)

        # große Zahlen
        l2 = [(545, "puck"), (700, "puck"), (285, "puck"), (746, "puck"), (546, "puck"), (145, "puck"),
                                     (689, "puck"), (273, "puck"), (682,"puck"), (361, "puck")]
        merge_sort(l2)
        sorted_2 = [(145, "puck"), (273, "puck"), (285, "puck"), (361, "puck"), (545, "puck"), (546, "puck"),
                                     (682, "puck"), (689, "puck"), (700,"puck"), (746, "puck")]
        self.assertEqual(l2, sorted_2)

        # kleine Zahlen
        l3 = [(1, "puck"), (0.12, "puck"), (0.7, "puck"), (0.35, "puck"), (1.1, "puck"), (0.36, "puck"),
                                     (0.2, "puck"), (0.73, "puck"), (0.41,"puck"), (1.3, "puck")]
        merge_sort(l3)
        sorted_3 = [(0.12, "puck"), (0.2, "puck"), (0.35, "puck"), (0.36, "puck"), (0.41, "puck"), (0.7, "puck"),
                                     (0.73, "puck"), (1, "puck"), (1.1,"puck"), (1.3, "puck")]
        self.assertEqual(l3, sorted_3)

    # testet Listen mit nur negativen Zahlen
    def test_negative_values(self):
        # kleine Zahlen
        l4 = [(-133, "puck"), (-47, "puck"), (-132, "puck"), (-47, "puck"), (-159, "puck"), (-38, "puck"),
                                     (-170, "puck"), (-145, "puck"), (-15,"puck"), (-100, "puck")]
        merge_sort(l4)
        sorted_4 = [(-170, "puck"), (-159, "puck"), (-145, "puck"), (-133, "puck"), (-132, "puck"), (-100, "puck"),
                                     (-47, "puck"), (-47, "puck"), (-38,"puck"), (-15, "puck")]
        self.assertEqual(l4, sorted_4)

        # große Zahlen
        l5 = [(-0.3, "puck"), (-0.56, "puck"), (-0.58, "puck"), (-0.58, "puck"), (-0.9, "puck"), (-0.9, "puck"),
                                     (-0.91, "puck"), (-1.3, "puck"), (-1.32,"puck"), (-2, "puck")]
        merge_sort(l5)
        sorted_5  =[(-2, "puck"), (-1.32, "puck"), (-1.3, "puck"), (-0.91, "puck"), (-0.9, "puck"), (-0.9, "puck"),
                                     (-0.58, "puck"), (-0.58, "puck"), (-0.56,"puck"), (-0.3, "puck")]
        self.assertEqual(l5, sorted_5)

    # testet Listen mit positiven und negativen Zahlen
    def test_mixed_values(self):
        l6 = [(0, "puck"), (-54.4, "puck"), (-100, "puck"), (0, "puck"), (-0.9, "puck"), (50, "puck"),
                                     (-54.5, "puck"), (-150, "puck"), (-12,"puck"), (0.56, "puck")]
        merge_sort(l6)
        sorted_6 = [(-150, "puck"), (-100, "puck"), (-54.5, "puck"), (-54.4, "puck"), (-12, "puck"), (-0.9, "puck"),
                                     (0, "puck"), (0, "puck"), (0.56,"puck"), (50, "puck")]
        self.assertEqual(l6, sorted_6)

