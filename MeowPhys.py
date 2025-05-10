import time, random, string, uuid
import dearpygui.dearpygui as dpg

def generate_random_string(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

class Vector2D:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
        
    def __add__(self, other: "Vector2D"):
        new_x = self.x + other.x
        new_y = self.y + other.y
        return Vector2D(new_x, new_y)

    def __sub__(self, other):
        new_x = self.x - other.x
        new_y = self.y - other.y
        return Vector2D(new_x, new_y)
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector2D(self.x * other, self.y * other)
        elif isinstance(other, Vector2D):
            return self.x * other.x + self.y * other.y
        else:
            raise TypeError("Unsupported type for multiplication")
    
    def __truediv__(self, n):
        new_x = self.x / n
        new_y = self.y / n
        return Vector2D(new_x, new_y)

    def norm(self):
        return ((self * self) ** 0.5)

g = Vector2D(0, 9.8)  
is_moving = False
coefficient_of_resistance = 0.6


class Figure(Vector2D):
    def __init__(self):
        return None
    
    def draw_in_pos(self, pos: Vector2D):
        pass


class Rectangle(Figure):
    def __init__(self, size = 10, pos = Vector2D(), picture = Figure()):
        self.pos = pos
        self.size = size
        self.picture = picture
        self.id = str(uuid.uuid4())
    
    def draw_in_pos(self, pos: Vector2D):
        self.pos.x = pos.x
        self.pos.y = pos.y
        left_up = [self.pos.x - self.size/2, self.pos.y - self.size/2]
        right_down = [self.pos.x + self.size/2, self.pos.y + self.size/2]
        dpg.delete_item(self.id)
        dpg.draw_rectangle(
            left_up, 
            right_down,
            color=(253, 217, 0, 255),  
            fill=(253, 217, 0, 200),
            tag=self.id,
            parent="canvas"
        )
    
    def contains_point(self, mouse_pos: Vector2D):
        #f"проверяет, попал ли курсор мыши в позиции {mouse_pos.x}, {mouse_pos.y} в область фигуры"
        half_size = self.size / 2
        if (self.pos.x - half_size <= mouse_pos.x <= self.pos.x + half_size):
            if (self.pos.y - half_size <= mouse_pos.y <= self.pos.y + half_size):
                return True
        return False

class Line(Figure):
    def __init__(self, pos_a = Vector2D(), pos_b = Vector2D()):
        self.pos_a = pos_a
        self.pos_b = pos_b

    def draw_in_pos(self, pos_start: Vector2D, pos_end: Vector2D):
        self.pos_a = pos_start
        self.pos_b = pos_end
        p1 = [self.pos_a.x, self.pos_a.y]
        p2 = [self.pos_b.x, self.pos_b.y]
        dpg.draw_line(
                p1,
                p2, 
                color=(240, 177, 178, 255), 
                thickness=3.0, 
                tag=str(uuid.uuid4()),
                parent="canvas"
            )


class Object:
    register = {}

    def __init__(self, picture = Rectangle(), mass = 1, velocity: Vector2D = Vector2D(0, 0)):
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
    
    def mouse_touch(self, meow_on):
        self.is_moving_local = False

    def draw_spring(self):
        for id in self._linkers:
            pos_end = Vector2D(self.pos.x, self.pos.y) # - self.picture.size / 2)
            Spring.register[id].line.draw_in_pos(Spring.register[id].pos, pos_end)
    

class Spring: #починить наледование (убрать его) 
    _counter = 0 
    register = {}

    def __init__(self, pos: Vector2D, k, line = Line()):
        self.pos = pos
        self.k = k
        self._L0_per_tag = {}
        self.line = line

        Spring._counter += 1
        self.tag = f"spring_{Spring._counter}" 
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
    

def handle_phys(o: Object):
    global is_moving, tick, speed_coef
    if o.is_moving_local and is_moving:
        a_old = o.acceleration
        o.pos = o.pos + (o.velocity * tick) + o.acceleration * ((tick**2)/ 2)
        o.acceleration = o.count_acceleration()
        o.velocity = o.velocity + (o.acceleration + a_old) * tick / 2
        o.draw_spring()
        o.picture.draw_in_pos(o.pos)

def change_moving():
    global is_moving
    is_moving ^= 1 #XOR 

def change_resistance():
    global resistance
    resistance ^= 1 #XOR 

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


resistance = False 
is_moving = True
speed_coef = 4
tick = 1/100 * speed_coef


dpg.create_context()
dpg.create_viewport(title='meow', width=800, height=600)

with dpg.window(tag="Main Window"):
    with dpg.group(horizontal=True):
        dpg.add_button(label="ON/OFF Moving", callback=change_moving)
        dpg.add_button(label="ON/OFF Resistance", callback=change_resistance)
    with dpg.drawlist(width=800, height=600, tag="canvas"):
        pass

dpg.setup_dearpygui()
dpg.show_viewport()

dpg.drawlist
o.picture.draw_in_pos(o.pos)
while dpg.is_dearpygui_running():
    if is_moving:
        dpg.delete_item("canvas", children_only=True)
        for id_obj in Object.register:
            handle_phys(Object.register[id_obj])
    dpg.render_dearpygui_frame()

dpg.destroy_context()