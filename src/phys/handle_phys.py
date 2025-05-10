from phys.Object import Object 
from config.const import is_moving, tick, resistance

def handle_phys(o: Object):
    global is_moving, tick
    if o.is_moving_local and is_moving:
        a_old = o.acceleration
        o.pos = o.pos + (o.velocity * tick) + o.acceleration * ((tick**2)/ 2)
        o.acceleration = o.count_acceleration()
        o.velocity = o.velocity + (o.acceleration + a_old) * tick / 2
        o.draw_spring()
        o.picture.draw_in_pos(o.pos)
