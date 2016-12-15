"""
SVG module
"""

class SVG:
    """
    SVG object
    """
    def __init__(self, width ,height):
        self.head = """<svg width="{}" height="{}">""".format(width, height)
        self.tail = "</svg>"
        self.svgs = []

    def save(self, filename):
        with open(filename, "w") as fsave:
            fsave.write(self.head)
            for svg in self.svgs:
                fsave.write(svg)
            fsave.write(self.tail)

    def add_line(self, point1, point2, couleur="rgb(255,0,0)", stroke_width=2):
        self.svgs.append("""<line x1="{}" y1="{}" x2="{}" y2="{}" style="color:{};stroke-width:{}" />""".
                            format(point1[0], point1[1], point2[0], point2[1], couleur, stroke_width))
