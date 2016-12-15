#!/usr/bin/env python3

"""
Module principal pour la découpe de modele 3D
"""

import argparse
import itertools
from stl import STL
from svg import SVG

def segment_intersects_slice(point0, point1, z_slice):
    """
    Calcul le parametre qui teste si les deux points forment un segment qui intersecte la tranche
    """
    denominateur = point1[2] - point0[2]
    numerateur = z_slice - point0[2]
    if denominateur != 0:
        parameter = numerateur/denominateur
        if parameter >= 0 and parameter <= 1:
            return parameter
    else:
        if numerateur == 0: #segment dans le plan
            return 'in'



def calcul_intersection(point0, point1, parameter):
    """
    Calcul du point d'intersection entre la tranche et le segment formé des deux points
    """
    return [point0[i] + parameter*(point1[i] - point0[i]) for i in range(3)]

def intersection(triangle, z_slice):
    """
    Iterateur sur les points d'intersection du triangle avec la tranche
    """
    points = []
    for couple in itertools.combinations(triangle.vertices, 2):
        parameter = segment_intersects_slice(couple[0], couple[1], z_slice)
        if parameter == 'in':
            points.append(couple[0])
            points.append(couple[1]) #marche si triangle dans plan ?
        elif parameter is not None:
            points.append(calcul_intersection(couple[0], couple[1], parameter))
    return points

def generate_slice(stl, z_slice, svg):
    """
    generation d'un tranche
    """
    for triangle in stl.triangles:
        points = intersection(triangle, z_slice)
        if points != []:
            # print(points) #temp
        # if len(points) == 1:
            # svg.point(filename, point[0])
        # elif len(points) >= 2:
            for couple in itertools.combinations(points, 2):
                # svg.segment(filename, points[0], points[1])
                svg.add_line(points[0], points[1])


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

    for index in range(args.SLICES):
        z_slice = z_start + height*index
        filename = "slice{}.svg".format(index)
        # svg.head(filename, dimension[0], dimension[1])
        svg = SVG(dimension[0], dimension[1])
        generate_slice(stl, z_slice, svg)
        # svg.tail(filename)
        svg.save(filename)

if __name__ == "__main__":
    main()
