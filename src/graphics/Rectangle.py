from phys.Vector2D import *
from graphics.Figure import * 
import uuid
import dearpygui.dearpygui as dpg
from config.const import is_moving

class Rectangle(Figure):
    register = {}
    def __init__(self, size = 100, pos = Vector2D()):
        self.pos = pos
        self.size = size
        self.id = str(uuid.uuid4())
        self.drag = 0
        self.register[self.id] = self
    
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
        half_size = self.size / 2
        if ((self.pos.x - half_size) <= mouse_pos.x <= (self.pos.x + half_size)):
            if ((self.pos.y - half_size) <= mouse_pos.y <= (self.pos.y + half_size)):
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
