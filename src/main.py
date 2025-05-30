import dearpygui.dearpygui as dpg
from phys.handle_phys import *
from phys import Object
from config.data import *
from config.const import *
from graphics.Rectangle import *

def change_moving(): #TODO перекинуть туда, где это будет уместнее
    global is_moving
    is_moving ^= 1 #XOR 

def drag_callback(sender, app_data):
    global is_moving
    offset = [0, 0]
    if dpg.is_mouse_button_down(dpg.mvMouseButton_Left):
        for id_obj in Object.register:
            o = Object.register[id_obj]
            r = Object.register[id_obj].picture
            mouse_pos = Vector2D(dpg.get_mouse_pos()[0], dpg.get_mouse_pos()[1])
            if (r.drag or r.contains_point(mouse_pos)):
                while dpg.is_mouse_button_down(dpg.mvMouseButton_Left):
                    mouse_pos = Vector2D(dpg.get_mouse_pos()[0], dpg.get_mouse_pos()[1])
                    if not r.drag:
                        offset = [mouse_pos.x - r.pos.x, mouse_pos.y - r.pos.y]
                        r.drag = True
                    o.pos = Vector2D(mouse_pos.x - offset[0], mouse_pos.y - offset[1])
                    dpg.delete_item(id_obj)
                    r.draw_in_pos(o.pos)
                    o.draw_spring()
                r.drag = False

dpg.create_context()
dpg.create_viewport(title='Simulation of vibrations of objects on springs', width=800, height=600)

with dpg.window(tag="Main Window"):
    with dpg.menu_bar():
        with dpg.menu(label="General"):
            dpg.add_button(label="ON/OFF Moving", callback=change_moving)
            dpg.add_button(label="ON/OFF Resistance", callback=change_resistance)
            dpg.add_slider_float(label="free fall acceleration", default_value=9.8, max_value=100, tag="free fall acceleration", callback=save_values)

        with dpg.menu(label="Object 1"):
            dpg.add_color_picker(label="Object 1 color", default_value=Color, tag='Object 1 color', callback=save_values)
            dpg.add_slider_float(label="Object 1 mass", default_value=20, max_value=100, tag="Object mass 1", callback=save_values)
        
        with dpg.menu(label="Object 2"):
            dpg.add_color_picker(label="Object 2 color", default_value=Color, tag='Object 2 color', callback=save_values)
            dpg.add_slider_float(label="Object 2 mass", default_value=30, max_value=100, tag="Object mass 2", callback=save_values)
        
        with dpg.menu(label='Springs'):
            dpg.add_slider_float(label='elastic coefficient 1', tag='s1', default_value=s1.k, max_value=30, callback=save_values)
            dpg.add_slider_float(label='elastic coefficient 2', tag='s2', default_value=s2.k, max_value=30, callback=save_values)
            dpg.add_color_picker(label="Spring 1 color", default_value=s1.line.color, tag='line 1 color', callback=save_values)
            dpg.add_color_picker(label="Spring 2 color", default_value=s2.line.color, tag='line 2 color', callback=save_values)
    
    
    dpg.add_drawlist(width=800, height=600, tag="canvas")
dpg.setup_dearpygui()
dpg.show_viewport()

with dpg.handler_registry():
    dpg.add_mouse_move_handler(callback=drag_callback)
    
while dpg.is_dearpygui_running():
    if is_moving:
        dpg.delete_item("canvas", children_only=True)
        for id_obj in Object.register:
            handle_phys(Object.register[id_obj])
        
    dpg.render_dearpygui_frame()

dpg.destroy_context()