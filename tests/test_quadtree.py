from simulator.quadtree import Point, QuadTree, Rectangle


def test_insert_out_of_bounds():
    qt = QuadTree(Rectangle(50, 50, 50, 50), 4) # x:0-100, y:0-100
    p = Point(150, 50)
    assert not qt.insert(p)
    assert len(qt.points) == 0

def test_boundary_overlap():
    qt = QuadTree(Rectangle(50, 50, 50, 50), 4)
    # Point exactly on the boundary x=100
    p = Point(100, 50)
    assert qt.insert(p)
    assert len(qt.points) == 1

def test_capacity_subdivision():
    qt = QuadTree(Rectangle(50, 50, 50, 50), 4)
    
    # Insert 4 points (reaches capacity)
    for i in range(4):
        assert qt.insert(Point(10 + i*5, 10 + i*5))
    
    assert not qt.divided
    assert len(qt.points) == 4
    
    # Insert 5th point to trigger subdivision
    assert qt.insert(Point(80, 80))
    
    assert qt.divided
    # Our optimized QuadTree pushes points down, so parent should be empty
    assert len(qt.points) == 0

def test_ghost_points_eaten():
    qt = QuadTree(Rectangle(50, 50, 50, 50), 4)
    p1 = Point(20, 20)
    p2 = Point(30, 30)
    qt.insert(p1)
    qt.insert(p2)
    
    # Mark one as eaten
    p1.eaten = True
    
    # Query the whole area
    found = qt.query(Rectangle(50, 50, 50, 50))
    
    # Should only return p2
    assert len(found) == 1
    assert found[0] == p2

def test_partial_queries():
    qt = QuadTree(Rectangle(50, 50, 50, 50), 2)
    
    qt.insert(Point(25, 25)) # SW
    qt.insert(Point(75, 25)) # SE
    qt.insert(Point(25, 75)) # NW
    qt.insert(Point(75, 75)) # NE
    
    assert qt.divided
    
    # Query box that overlaps SW, SE, and NW slightly, but not NE
    # Center at (40, 40), width/height 20 -> x: 20-60, y: 20-60
    query_box = Rectangle(40, 40, 20, 20)
    found = qt.query(query_box)
    
    # Should find SW (25, 25)
    assert len(found) == 1
    assert found[0].x == 25 and found[0].y == 25
