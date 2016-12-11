#!/usr/bin/env python3

"""
Module principal pour la découpe de modele 3D
"""

import argparse
from stl import STL


def main():
    """
    Fonction principale
    """
    parser = argparse.ArgumentParser(description="slice a binary STL file")
    parser.add_argument("stl_file", help="name of the binary STL file to slice")
    parser.add_argument("-s", "--slices", type=int, dest="SLICES", default=4,
                        help="how many slices you want (default = 4)")
    args = parser.parse_args()

    stl = STL()
    stl.load(args.stl_file)
    dimension, z_start = stl.dimensions()
    height = dimension[2]/args.SLICES

if __name__ == "__main__":
    main()
