#!/usr/bin/env python3

"""
Module principal pour la découpe de modèles 3D
"""

import argparse
import itertools
from stl import STL
from svg import SVG


def triangle_in_slice(triangle, z_slice):
    """
    Teste si le triangle est dans la tranche
    """
    return sum(1 for point in triangle if point[2] == z_slice) // 3


def segment_in_slice(point0, point1, z_slice):
    """
    Teste si le segment est dans la tranche
    """
    return point0[2] == z_slice and point1[2] == z_slice


def segment_intersects_slice(point0, point1, z_slice):
    """
    Calcule le parametre qui teste si les deux points forment un segment qui intersecte la tranche
    """
    denominateur = point1[2] - point0[2]
    numerateur = z_slice - point0[2]
    if denominateur != 0:
        parameter = numerateur/denominateur
        if parameter >= 0 and parameter <= 1:
            return parameter


def calcul_intersection(point0, point1, parameter):
    """
    Calcul du point d'intersection entre la tranche et le segment formé des deux points
    """
    return [point0[i] + parameter*(point1[i] - point0[i]) for i in range(3)]


def intersection(triangle, z_slice):
    """
    Calcul des points d'intersection du triangle avec la tranche
    """
    points = []
    for point0, point1 in itertools.combinations(triangle.vertices, 2):
        if segment_in_slice(point0, point1, z_slice) and not triangle_in_slice(triangle, z_slice):
            points.append(point0)
            points.append(point1)
        else:
            parameter = segment_intersects_slice(point0, point1, z_slice)
            if parameter:
                points.append(calcul_intersection(point0, point1, parameter))
    return points


def generate_slice(stl, z_slice, svg, origins, scale):
    """
    Generation d'un tranche
    """
    for triangle in stl.triangles:
        points = intersection(triangle, z_slice)
        for point0, point1 in itertools.combinations(points, 2):
            for index in range(2):
                point0[index] = (point0[index] - origins[index])*scale
                point1[index] = (point1[index] - origins[index])*scale
            svg.add_line(point0, point1)


def main():
    """
    Fonction principale
    """
    parser = argparse.ArgumentParser(description="slice a binary STL file")
    parser.add_argument("stl_file", help="name of the binary STL file to slice")
    parser.add_argument("-s", "--slices", type=int, dest="SLICES", default=4,
                        help="how many slices you want (default is 4)")
    parser.add_argument("-g", "--grow", type=int, dest="SCALE", default=100,
                        help="scale up or down the slices (default is scale up by 100)")
    args = parser.parse_args()

    stl = STL()
    stl.load(args.stl_file)
    dimension, origins = stl.dimensions()
    height = dimension[2]/args.SLICES

    for index in range(args.SLICES):
        z_slice = origins[2] + height*index
        filename = "slice{}.svg".format(index)
        svg = SVG(dimension[0]*args.SCALE, dimension[1]*args.SCALE)
        generate_slice(stl, z_slice, svg, origins, args.SCALE)
        svg.save(filename)


if __name__ == "__main__":
    main()
