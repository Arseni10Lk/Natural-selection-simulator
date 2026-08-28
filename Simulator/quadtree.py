class Point:
    __slots__ = ['x', 'y', 'eaten']
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.eaten = False

class Rectangle:
    __slots__ = ['x', 'y', 'w', 'h']
    def __init__(self, x, y, w, h):
        self.x = x  # center x
        self.y = y  # center y
        self.w = w  # half width
        self.h = h  # half height

    def contains(self, point):
        return (self.x - self.w <= point.x <= self.x + self.w and
                self.y - self.h <= point.y <= self.y + self.h)

    def intersects(self, range_rect):
        if isinstance(range_rect, Circle):
            return range_rect.intersects(self)
            
        return not (range_rect.x - range_rect.w > self.x + self.w or
                    range_rect.x + range_rect.w < self.x - self.w or
                    range_rect.y - range_rect.h > self.y + self.h or
                    range_rect.y + range_rect.h < self.y - self.h)

class Circle:
    __slots__ = ['x', 'y', 'r']
    def __init__(self, x, y, r):
            self.x = x  # center x
            self.y = y  # center y
            self.r = r  # radius
    def contains(self, point):
        # Pythagorean theorem (squared) to check true circular distance
        return (point.x - self.x)**2 + (point.y - self.y)**2 <= self.r**2
    
    def intersects(self, range_rect):
            # Find the closest X and Y point on the rectangle to the circle's center
            closest_x = max(range_rect.x - range_rect.w, min(self.x, range_rect.x + range_rect.w))
            closest_y = max(range_rect.y - range_rect.h, min(self.y, range_rect.y + range_rect.h))

            # Calculate the squared distance from the circle center to that closest point
            distance_x = self.x - closest_x
            distance_y = self.y - closest_y

            return (distance_x**2 + distance_y**2) <= self.r**2

class QuadTree:
    def __init__(self, boundary, capacity):
        self.boundary = boundary
        self.capacity = capacity
        self.points = []
        self.divided = False
        self.nw = None
        self.ne = None
        self.sw = None
        self.se = None

    def subdivide(self):
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
            self.ne.insert(p) or self.nw.insert(p) or self.se.insert(p) or self.sw.insert(p)
        self.points = []

    def insert(self, point):
        if not self.boundary.contains(point):
            return False

        if len(self.points) < self.capacity and not self.divided:
            self.points.append(point)
            return True
        
        if not self.divided:
            self.subdivide()

        return (self.ne.insert(point) or 
                self.nw.insert(point) or 
                self.se.insert(point) or 
                self.sw.insert(point))

    def query(self, range_rect, found=None):
        if found is None:
            found = []

        if not self.boundary.intersects(range_rect):
            return found

        if self.divided:
            self.nw.query(range_rect, found)
            self.ne.query(range_rect, found)
            self.sw.query(range_rect, found)
            self.se.query(range_rect, found)
        else:
            for p in self.points:
                if not p.eaten and range_rect.contains(p):
                    found.append(p)

        return found
