from phys.Vector2D import Vector2D
import Figure, uuid
import dearpygui.dearpygui as dpg

class Line:
    def __init__(self, pos_a: Vector2D, pos_b: Vector2D, color = [240, 177, 178, 255]):
        self.pos_a = pos_a
        self.pos_b = pos_b
        self.color = color
    def draw_in_pos(self, pos_start: Vector2D, pos_end: Vector2D):
        self.pos_a = pos_start
        self.pos_b = pos_end
        p1 = [self.pos_a.x, self.pos_a.y]
        p2 = [self.pos_b.x, self.pos_b.y]
        dpg.draw_line(
                p1,
                p2, 
                color=self.color, 
                thickness=3.0, 
                tag=str(uuid.uuid4()),
                parent="canvas"
            )