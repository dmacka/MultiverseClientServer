import ClientAPI

class RegionPoint:
    def __init__(self, x, z):
        self.x = x
        self.z = z
        
    def __repr__(self):
        return 'RegionPoint(%f,%f)' % (self.x, self.z)

# determine if the two line segments defined by (p1, p2) and (p3,p4) intersect
def _intersectSegments(p1, p2, p3, p4):
    den = ((p4.z - p3.z) * (p2.x - p1.x)) - ((p4.x - p3.x) * (p2.z - p1.z))
    t1num = ((p4.x - p3.x) * (p1.z - p3.z)) - ((p4.z - p3.z) * (p1.x - p3.x))
    t2num = ((p2.x - p1.x) * (p1.z - p3.z)) - ((p2.z - p1.z) * (p1.x - p3.x))
    
    if den == 0.0:
        return False
        
    t1 = t1num / den
    t2 = t2num / den
    
    if (t1 >= 0.0) and (t1 < 1.0) and (t2 >= 0.0) and (t2 <= 1.0):
        return True
        
    return False
            
class Region:
    def __init__(self, pointsIn):
        # create points list
        self.points = []
        
        # add points to the list
        for point in pointsIn:
            self.points.append(RegionPoint(point.x, point.z))
            
        self._computeBounds()

    def __repr__(self):
        retstr = 'Bounds:\n\tMin: %s\n\tMax: %s\nPoints:\n' % (str(self.minBound), str(self.maxBound))
        for point in self.points:
            retstr = retstr + '\t%s\n' %str(point)
        return retstr
                 
    # compute the bounding rectangle of the region
    def _computeBounds(self):
        if len(self.points) > 1:
            self.minBound = RegionPoint(self.points[0].x, self.points[0].z)
            self.maxBound = RegionPoint(self.points[0].x, self.points[0].z)
            for point in self.points:
                if point.x < self.minBound.x:
                    self.minBound.x = point.x
                if point.x > self.maxBound.x:
                    self.maxBound.x = point.x
                if point.z < self.minBound.z:
                    self.minBound.z = point.z
                if point.z > self.maxBound.z:
                    self.maxBound.z = point.z

    # is the given point within the bounding box of the region
    def _pointInBounds(self, p):
        if p.x <= self.minBound.x or p.x > self.maxBound.x or p.z < self.minBound.z or p.z > self.maxBound.z:
            return False
        return True
        
    def PointIn(self, point):
        crossings = 0
    
        if self._pointInBounds(point):
            topPoint = RegionPoint(point.x, self.maxBound.z)
            
            for i in range(len(self.points) - 1):
                if _intersectSegments(self.points[i], self.points[i + 1], point, topPoint):
                    crossings = crossings + 1
                if _intersectSegments(self.points[-1], self.points[0], point, topPoint):
                    crossings = crossings + 1
        return (crossings & 1) == 1
        
    #
    # returns a random point in the region
    #
    def RandomPoint(self):
        rangeX = self.maxBound.x - self.minBound.x
        rangeZ = self.maxBound.z - self.minBound.z
        
        found = False
        
        # search for a random point that is in the region
        while not found:
            x = ClientAPI.RandomFloat(rangeX) + self.minBound.x
            z = ClientAPI.RandomFloat(rangeZ) + self.minBound.z
        
            pt = RegionPoint(x, z)
        
            found = self.PointIn(pt)
        
        return pt
        
#
# region test code below
#           
def TestPoint(testReg, pt):
    print 'Testing %s' % str(pt)
    print '  returns %s' % str(testReg.PointIn(pt))

def _test():    
    testRegion = [
            RegionPoint(5.0, 0.0),
            RegionPoint(0.0, 5.0),
            RegionPoint(45.0, 50.0),
            RegionPoint(50.0, 45.0)
            ]
    testReg = Region(testRegion)
    print testReg

    TestPoint(testReg, RegionPoint(25.0, 25.0))
    TestPoint(testReg, RegionPoint(0.0, 0.0))
    TestPoint(testReg, RegionPoint(1.0, 1.0))
    TestPoint(testReg, RegionPoint(20.0, 10.0))
    TestPoint(testReg, RegionPoint(10.0, 10.0))
    TestPoint(testReg, RegionPoint(-5.0, 25.0))
    TestPoint(testReg, RegionPoint(30.0, 32.0))
    TestPoint(testReg, RegionPoint(47.0, 49.0))

#_test()
