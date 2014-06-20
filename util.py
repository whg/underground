import math, random

class Station:
    def __init__(self, name, lines=[], loc=(0,0)):
        self.name = name
        self.lines = lines
        self.loc = loc
        self.pos = None

    def __repr__(self):
        return '%s: %s' % (self.name, self.pos)

class Journey:
    def __init__(self, route=[], stops=[], changes=0, dist=0, sjns=[]):
        #route: [start, (line, intermediate_station)*, line, end]
        self.route = route
        #stops: [start, station*, end]
        self.stops = stops
        #number of changes
        self.changes = changes
        #sum of as the crow flies distance between stops
        self.dist = dist
        #a simple ranking...
        self.rank = len(stops) * (changes+1) * dist
        #separate journeys
        self.sjns = sjns        

class Vector:
    '''very simple vector class, doing just what we need'''
    def __init__(self, t=(0, 0),x=0.0, y=0.0):
        self.x = x
        self.y = y
        self.x, self.y = t
                
    def __repr__(self):
        '''for pretty printing'''
        return "(%.2f, %.2f)" % (self.x, self.y)
    
    def __sub__(self, v):
        return Vector((self.x - v.x, self.y - v.y))
        
    def __add__(self, v):
        return Vector((self.x + v.x, self.y + v.y))
        
    def __div__(self, s):
        return Vector((self.x/s, self.y/s))
    
    def __mul__(self, s):
        return Vector((self.x*s, self.y*s))
        
    def mag(self):
        return math.sqrt(self.x**2 + self.y**2)
    
    def norm(self):
        m = self.mag()
        return Vector((self.x/m, self.y/m))
    
    def normalize(self):
        '''this differs to norm(), as it normalises the vector in place'''
        m = self.mag()
        self.x/= m
        self.y/= m
        
    def dot(self, v):
        return self.x*v.x + self.y*v.y
        
    def angle(self, v):
            '''returns 5 it's going to try and divide by zero'''
            if v.x == 0.0 and v.y == 0.0:
                return 5
            elif self.x == 0.0 and self.y == 0.0:
                return 5
            return math.acos(min(1.0, self.dot(v)/(self.mag()*v.mag())))
        
    def addnoise(self, sigma=0.5):
        '''add gaussian noise to both components'''
        self.x+= random.gauss(0, sigma)
        self.y+= random.gauss(0, sigma)
        return self

