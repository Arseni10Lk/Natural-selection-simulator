from __future__ import annotations


class Point:
    __slots__ = ['eaten', 'x', 'y']
    x: float
    y: float
    eaten: bool

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        self.eaten = False

class Rectangle:
    __slots__ = ['h', 'w', 'x', 'y']
    x: float
    y: float
    w: float
    h: float

    def __init__(self, x: float, y: float, w: float, h: float) -> None:
        self.x = x  # center x
        self.y = y  # center y
        self.w = w  # half width
        self.h = h  # half height

    def contains(self, point: Point) -> bool:
        return (self.x - self.w <= point.x <= self.x + self.w and
                self.y - self.h <= point.y <= self.y + self.h)

    def intersects(self, range_rect: Rectangle | Circle) -> bool:
        if isinstance(range_rect, Circle):
            return range_rect.intersects(self)
            
        return not (range_rect.x - range_rect.w > self.x + self.w or
                    range_rect.x + range_rect.w < self.x - self.w or
                    range_rect.y - range_rect.h > self.y + self.h or
                    range_rect.y + range_rect.h < self.y - self.h)

class Circle:
    __slots__ = ['r', 'x', 'y']
    x: float
    y: float
    r: float

    def __init__(self, x: float, y: float, r: float) -> None:
        self.x = x  # center x
        self.y = y  # center y
        self.r = r  # radius

    def contains(self, point: Point) -> bool:
        # Pythagorean theorem (squared) to check true circular distance
        return (point.x - self.x)**2 + (point.y - self.y)**2 <= self.r**2
    
    def intersects(self, range_rect: Rectangle) -> bool:
        # Find the closest X and Y point on the rectangle to the circle's center
        closest_x = max(range_rect.x - range_rect.w, min(self.x, range_rect.x + range_rect.w))
        closest_y = max(range_rect.y - range_rect.h, min(self.y, range_rect.y + range_rect.h))

        # Calculate the squared distance from the circle center to that closest point
        distance_x = self.x - closest_x
        distance_y = self.y - closest_y

        return (distance_x**2 + distance_y**2) <= self.r**2

class QuadTree:
    boundary: Rectangle
    capacity: int
    points: list[Point]
    divided: bool
    nw: QuadTree | None
    ne: QuadTree | None
    sw: QuadTree | None
    se: QuadTree | None

    def __init__(self, boundary: Rectangle, capacity: int) -> None:
        self.boundary = boundary
        self.capacity = capacity
        self.points = []
        self.divided = False
        self.nw = None
        self.ne = None
        self.sw = None
        self.se = None

    def subdivide(self) -> None:
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w / 2
        h = self.boundary.h / 2

        self.ne = QuadTree(Rectangle(x + w, y + h, w, h), self.capacity)
        self.nw = QuadTree(Rectangle(x - w, y + h, w, h), self.capacity)
        self.se = QuadTree(Rectangle(x + w, y - h, w, h), self.capacity)
        self.sw = QuadTree(Rectangle(x - w, y - h, w, h), self.capacity)
        self.divided = True

        # Push existing points down to children
        for p in self.points:
            # We assert they are not None because we just created them
            assert self.ne and self.nw and self.se and self.sw
            self.ne.insert(p) or self.nw.insert(p) or self.se.insert(p) or self.sw.insert(p)
        self.points = []

    def insert(self, point: Point) -> bool:
        if not self.boundary.contains(point):
            return False

        if len(self.points) < self.capacity and not self.divided:
            self.points.append(point)
            return True
        
        if not self.divided:
            self.subdivide()

        assert self.ne and self.nw and self.se and self.sw
        return (self.ne.insert(point) or 
                self.nw.insert(point) or 
                self.se.insert(point) or 
                self.sw.insert(point))

    def query(self, range_rect: Rectangle | Circle, found: list[Point] | None = None) -> list[Point]:
        if found is None:
            found = []

        if not self.boundary.intersects(range_rect):
            return found

        if self.divided:
            assert self.nw and self.ne and self.sw and self.se
            self.nw.query(range_rect, found)
            self.ne.query(range_rect, found)
            self.sw.query(range_rect, found)
            self.se.query(range_rect, found)
        else:
            for p in self.points:
                if not p.eaten and range_rect.contains(p):
                    found.append(p)

        return found
