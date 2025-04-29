from graphics import Rectangle
from phys.Vector2D import *
from phys.Object import *
from phys.Spring import *

r = Rectangle(100, Vector2D(600, 100))
r1 = Rectangle(60, Vector2D(300, 100))
o = Object(r, 30)
o1 = Object(r1, 20)
s1 = Spring(Vector2D(200, 200), 10)
s2 = Spring(Vector2D(700, 200), 7)
s1.link(o)
s2.link(o)
s1.link(o1)
s2.link(o1)