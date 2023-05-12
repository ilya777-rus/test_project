import math
from typing import List


class StandardLine(object):
    """
    A line in a coordinate grid described in standard form (ax + by = c).
    """
    def __init__(self, x_quantifier: float, y_quantifier: float, equates: float):
        """
        A line in a coordinate grid described in standard form (ax + by = c).

        :param x_quantifier: variable a of the equation
        :param y_quantifier: variable b of the equation
        :param equates: variable c of the equation
        """
        self.x_quantifier = x_quantifier
        self.y_quantifier = y_quantifier
        self.equates = equates

    def __str__(self) -> str:
        return f"{self.A}x + {self.B}y = {self.C}"

    @property
    def A(self) -> float:
        return self.x_quantifier

    @property
    def B(self) -> float:
        return self.y_quantifier

    @property
    def C(self) -> float:
        return self.equates


class Coordinate(object):
    """
    A single x or y coordinate that doesn't have a specific value yet.
    """
    def __init__(self, _min: float, _max: float):
        self.min = _min
        self.max = _max

    @property
    def diff(self) -> float:
        return self.max - self.min

    @property
    def center(self) -> float:
        return self.min + self.diff * 0.5


class Vertex(object):
    """
    A Vertex - a point in 2D space described by an x and y value.
    """
    def __init__(self, x: float, y: float):
        """
        A Vertex - a point in 2D space described by an x and y value.

        :param x: the x coordinate of the vertex
        :param y: the y coordinate of the vertex
        """
        self.x = x
        self.y = y

    # def __json__(self):
    #     return {
    #         'x': self.x,
    #         'y': self.y,
    #     }

    def __getitem__(self, item) -> float:
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        else:
            raise IndexError

    def __eq__(self, other) -> bool:
        if isinstance(other, Vertex):
            if self.x == other.x and self.y == other.y:
                return True
            else:
                return False
        else:
            raise AssertionError(f"Cannot compare Vertex to {other.__class__}")

    def __sub__(self, other):
        if isinstance(other, Vertex):
            return Vertex(
                x=self.x - other.x,
                y=self.y - other.y
            )
        elif isinstance(other, int):
            return Vertex(
                x=self.x - other,
                y=self.y - other,
            )
        elif isinstance(other, float):
            return Vertex(
                x=self.x - other,
                y=self.y - other,
            )
        else:
            raise SyntaxError(f"Cannot subtract {other.__class__} from Vertex")

    def __add__(self, other):
        if isinstance(other, Vertex):
            return Vertex(
                x=self.x + other.x,
                y=self.y + other.y
            )
        elif isinstance(other, int):
            return Vertex(
                x=self.x + other,
                y=self.y + other,
            )
        elif isinstance(other, float):
            return Vertex(
                x=self.x + other,
                y=self.y + other,
            )
        else:
            raise SyntaxError(f"Cannot add {other.__class__} to Vertex")

    def __truediv__(self, other):
        if isinstance(other, Vertex):
            return Vertex(
                x=self.x / other.x,
                y=self.y / other.y
            )
        elif isinstance(other, int) or isinstance(other, float):
            return Vertex(
                x=self.x / other,
                y=self.y / other,
            )
        else:
            raise SyntaxError(f"Cannot divide Vertex by {other.__class__}")

    def __abs__(self):
        return Vertex(
            x=abs(self.x),
            y=abs(self.y),
        )

    @property
    def to_tuple(self) -> tuple:
        """
        :return: the vertex represented as an (x, y) tuple
        """
        return tuple([self.x, self.y])

    def distance_to(self, other) -> float:
        """
        A helper method to calculate the distance to another vertex using pythagoras

        :param other: the vertex to calculate the distance to.
        :return: the calculated distance.
        """
        if isinstance(other, Vertex):
            pythagorean_vertex = self - other
            square_distance = pythagorean_vertex.x ** 2 + pythagorean_vertex.y ** 2
            rooted_distance = math.sqrt(square_distance)
            return rooted_distance
        else:
            raise SyntaxError(f"Cannot calculate distance between Vertex and {other.__class__}")


class Edge(object):
    """
    An Edge - a line(AB) in 2D space described by 2 vertices
    """
    def __init__(self, a: Vertex, b: Vertex):
        """
        An Edge - a line in 2D space described by by 2 vertices

        :param a: vertex a of the line
        :param b: vertex b of the line
        """
        self.a = a
        self.b = b

    def __getitem__(self, item) -> Vertex:
        if item == 0:
            return self.a
        elif item == 1:
            return self.b
        else:
            raise IndexError

    def __eq__(self, other) -> bool:
        if isinstance(other, Edge):
            if self.a == other.a and self.b == other.b:
                return True
            elif self.b == other.a and self.a == other.b:
                return True
            return False
        else:
            raise AssertionError(f"Cannot compare Edge to {other.__class__}")

    @property
    def vertices(self) -> List[Vertex]:
        """
        :return: a list containing the edges vertices
        """
        return [self.a, self.b]


class Triangle(object):
    """
    A Triangle represented as 3 vertices a, b, c
    """

    def __init__(self, a: Vertex, b: Vertex, c: Vertex, is_super: bool = False):
        """
        A Triangle represented as as 3 vertices a, b, c

        :param a: vertex a of the triangle
        :param b: vertex b of the triangle
        :param c: vertex c of the triangle
        :param is_super: triangle is a super triangle
        """
        self.a = a
        self.b = b
        self.c = c
        self.is_super = is_super

    def __getitem__(self, item) -> Vertex:
        if item == 0:
            return self.a
        elif item == 1:
            return self.b
        elif item == 2:
            return self.c
        else:
            raise IndexError

    def __eq__(self, other) -> bool:
        if isinstance(other, Triangle):
            if self.a == other.a and self.b == other.b and self.c == other.c:
                return True
            return False
        else:
            raise AssertionError(f"Cannot compare Triangle to {other.__class__}")

    @property
    def ab_center(self) -> Vertex:
        """
        :return: the center vertex of the triangles Edge(AB)
        """
        return (self.a + self.b) / 2

    @property
    def bc_center(self) -> Vertex:
        """
        :return: the center vertex of the triangles Edge(BA)
        """
        return (self.b + self.c) / 2

    @property
    def ca_center(self) -> Vertex:
        """
        :return: the center vertex of the triangles Edge(CA)
        """
        return (self.c + self.a) / 2

    @property
    def ab_edge(self) -> Edge:
        """
        :return: the triangles Edge(AB)
        """
        return Edge(a=self.a, b=self.b)

    @property
    def bc_edge(self) -> Edge:
        """
        :return: the triangles Edge(BA)
        """
        return Edge(a=self.b, b=self.c)

    @property
    def ca_edge(self) -> Edge:
        """
        :return: the triangles Edge(CA)
        """
        return Edge(a=self.c, b=self.a)

    @property
    def vertices(self) -> List[Vertex]:
        """
        :return: a list of all vertices contained in this triangle
        """
        return [self.a, self.b, self.c]

    @property
    def edges(self) -> List[Edge]:
        """
        :return: a list of all edges contained in this triangle
        """
        return [self.ab_edge, self.bc_edge, self.ca_edge]

    @property
    def circumcenter(self) -> Vertex:
        """
        :return: the circumcenter of this triangle
        """
        ab = get_standard_line(p=self.a, q=self.b)
        bc = get_standard_line(p=self.b, q=self.c)

        pb_ab = get_perpendicular_bisector(p=self.a, q=self.b, line=ab)
        pb_bc = get_perpendicular_bisector(p=self.b, q=self.c, line=bc)

        return get_line_intersection(l1=pb_ab, l2=pb_bc)

    @property
    def circumradius(self) -> float:
        """
        :return: the circumradius of this triangle
        """
        return self.circumcenter.distance_to(self.a)

    @property
    def circumcircle(self):
        """
        :return: the circumcircle of this triangle
        """
        return Circle(center=self.circumcenter, radius=self.circumradius)


class Circle(object):
    """
    A Circle described by its center and its radius
    """
    def __init__(self, center: Vertex, radius: float):
        """
        A Circle described by its center and its radius

        :param center: the center of the circle
        :param radius: the radius of the circle
        """
        self.center = center
        self.radius = radius

    def encompasses_vertex(self, vertex: Vertex) -> bool:
        if self.radius >= self.center.distance_to(vertex):
            return True
        else:
            return False

    @property
    def top_left_circumsquare_corner(self):
        return tuple([self.center.x - self.radius, self.center.y - self.radius])

    @property
    def bottom_right_circumsquare_corner(self):
        return tuple([self.center.x + self.radius, self.center.y + self.radius])


def get_standard_line(p: Vertex, q: Vertex) -> StandardLine:
    """
    Create a StandardLine from 2 vertices

    :param p: vertex p of the StandardLine
    :param q: vertex q of the StandardLine
    :return: a StandardLine created from the given 2 vertices
    """

    a = q.y - p.y
    b = p.x - q.x
    c = a * p.x + b * p.y
    return StandardLine(
        x_quantifier=a,
        y_quantifier=b,
        equates=c
    )


def get_perpendicular_bisector(p: Vertex, q: Vertex, line: StandardLine) -> StandardLine:
    mid_point = (p + q) / 2
    c = -line.B * mid_point.x + line.A * mid_point.y
    a = -line.B
    b = line.A
    return StandardLine(
        x_quantifier=a,
        y_quantifier=b,
        equates=c
    )


def get_line_intersection(l1: StandardLine, l2: StandardLine) -> Vertex:
    """
    Get the intersection Vertex of 2 StandardLines

    :param l1: StandardLine l1
    :param l2: StandardLine l2
    :return: the intersection Vertex between l1 and l2
    """
    determinant = l1.A * l2.B - l2.A * l1.B
    if determinant == 0:  # The lines are parallel
        raise ValueError(f"The lines {l1} and {l2} do not intersect.")
    else:
        return Vertex(
            x=(l2.B * l1.C - l1.B * l2.C) / determinant,
            y=(l1.A * l2.C - l2.A * l1.C) / determinant
        )
