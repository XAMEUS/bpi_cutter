"""
STL module
"""
import struct

class Triangle:
    """
    STL Triangle
    REAL32[3] – Normal vector
    REAL32[3] – Vertex 1
    REAL32[3] – Vertex 2
    REAL32[3] – Vertex 3
    UINT16 – Attribute byte count
    """
    def __init__(self):
        self.normal_vector = None
        self.vertices = ()
        self.attribute = None

class STL:
    """
    STL object
    """
    def __init__(self):
        self.triangles = []
        self.header = ""

    def __str__(self):
        return self.header + "\n" + str(len(self.triangles)) + " triangles"

    def load(self, filename):
        """
        :param filename: the file's name
        """
        self.triangles = []
        self.header = ""
        with open(filename, 'rb') as stl:
            for _ in range(80):
                self.header += struct.unpack('c', stl.read(1))[0].decode("utf-8")
            for _ in range(struct.unpack('i', stl.read(4))[0]):
                triangle = Triangle()
                triangle.normal_vector = struct.unpack('f'*3, stl.read(4*3))
                vertex1 = struct.unpack('f'*3, stl.read(4*3))
                vertex2 = struct.unpack('f'*3, stl.read(4*3))
                vertex3 = struct.unpack('f'*3, stl.read(4*3))
                triangle.vertices = (vertex1, vertex2, vertex3)
                triangle.attribute = struct.unpack('h', stl.read(2))[0]
                self.triangles.append(triangle)
