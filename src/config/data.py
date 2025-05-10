from graphics import Rectangle
from phys.Vector2D import *
from phys.Object import *
from phys.Spring import *
from config.const import *

def save_values(sender, app_data):
    g.y = dpg.get_value("free fall acceleration")
    o1.picture.color = dpg.get_value('Object 1 color')
    o.picture.color =  dpg.get_value('Object 2 color')
    o.mass = dpg.get_value('Object mass 2')
    o1.mass = dpg.get_value('Object mass 1')
    s1.k = dpg.get_value('s1')
    s2.k = dpg.get_value('s2')
    s1.line.color = dpg.get_value('line 1 color')
    s2.line.color = dpg.get_value('line 2 color')

r = Rectangle(100, Vector2D(600, 100))
r1 = Rectangle(60, Vector2D(300, 100))
o = Object(r, 30)
o1 = Object(r1, 20)
s1 = Spring(Vector2D(200, 200), 10, Line(Vector2D(200, 200), Vector2D(200, 200)))
s2 = Spring(Vector2D(700, 200), 7, Line(Vector2D(700, 200), Vector2D(700, 200)))
s1.link(o)
s2.link(o)
s1.link(o1)
s2.link(o1)