#!/usr/bin/env python3
"""
Unit tests
"""

import unittest
from stl import STL

class TestSTL(unittest.TestCase):
    """
    Unit tests
    """
    def test_load_stl(self):
        """
        loading test
        """
        stl = STL()
        stl.load("models/Tux_printable.stl")
        self.assertEqual(len(stl.triangles), 14842)
        stl.load("models/Pumpkin_whole.stl")
        self.assertEqual(len(stl.triangles), 138282)

if __name__ == "__main__":
    unittest.main(verbosity=2)
