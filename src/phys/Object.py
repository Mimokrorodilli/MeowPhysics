from phys.Vector2D import *
import uuid
# from phys.Spring import Spring
from graphics.Rectangle import *
from config.const import *

class Object:
    register = {}

    def __init__(self, picture: Rectangle, mass = 1, velocity: Vector2D = Vector2D(0, 0)):
        self.pos = picture.pos
        self.picture = picture
        self.mass = mass
        self.velocity = velocity
        self._linkers = []
        self.is_moving_local = True
        self.acceleration = Vector2D(0, 0)

        self.tag = str(uuid.uuid4())
        Object.register[self.tag] = self

    def put_link(self, s):
        self._linkers.append(s)

    def count_acceleration(self):
        F_of_resistance = Vector2D(0, 0)
        if resistance:
            if self.velocity.norm() != 0:
                F_of_resistance = self.velocity * 0.15 * 1.2 * (self.velocity * self.velocity) / self.velocity.norm()
        F_r = g * self.mass - F_of_resistance
        for id in self._linkers:
            F_r = F_r + Spring.register[id].count_elastic_force(self)
        return((F_r / self.mass))
    
    def mouse_touch(self):
        self.is_moving_local = False

    def draw_spring(self):
        for id in self._linkers:
            pos_end = Vector2D(self.pos.x, self.pos.y)
            Spring.register[id].line.draw_in_pos(Spring.register[id].pos, pos_end)


class Spring: #починить наледование (убрать его нахуй) 
    register = {}

    def __init__(self, pos: Vector2D, k, line = Line()):
        self.pos = pos
        self.k = k
        self._L0_per_tag = {}
        self.line = line

        self.tag = str(uuid.uuid4())
        Spring.register[self.tag] = self

    def link(self, A: Object):
        l_0 = (A.pos - self.pos) #подбираем пружинку длины l_0
        A.put_link(self.tag)
        self._L0_per_tag[A.tag] = l_0

    def count_elastic_force(self, A: Object) -> Vector2D:
        current_l = A.pos - self.pos
        direction = current_l / current_l.norm()
        F_e = direction * (current_l.norm() - self._L0_per_tag[A.tag].norm()) * self.k
        return F_e * (-1)