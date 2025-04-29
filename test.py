import uuid
import dearpygui.dearpygui as dpg

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

class Figure:
    def __init__(self):
        pass
    
    def draw_in_pos(self, pos: Vector2D):
        pass

class Rectangle(Figure):
    def __init__(self, size, pos: Vector2D):
        self.pos = pos
        self.size = size
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
print('oaoaoaoaoaoao')
dpg.create_context()
dpg.create_viewport(title='meow', width=800, height=600)

with dpg.window(tag="Main Window"):
    dpg.add_drawlist(width=800, height=600, tag="canvas")

dpg.setup_dearpygui()
dpg.show_viewport()

r = Rectangle(100, Vector2D(400, 100))

while dpg.is_dearpygui_running():
    r.draw_in_pos(r.pos)
    dpg.render_dearpygui_frame()

dpg.destroy_context()