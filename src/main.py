import dearpygui.dearpygui as dpg
from phys.handle_phys import *
from phys import Object
from config.data import *
from config.const import *

def change_moving(): #TODO: перекинуть туда, где это будет уместнее
    global is_moving
    is_moving ^= 1 #XOR 

def change_resistance():
    global resistance
    resistance ^= 1 #XOR 

dpg.create_context()
dpg.create_viewport(title='meow', width=800, height=600)

with dpg.window(tag="Main Window"):
    with dpg.group(horizontal=True):
        dpg.add_button(label="ON/OFF Moving", callback=change_moving)
        dpg.add_button(label="ON/OFF Resistance", callback=change_resistance)
    dpg.add_drawlist(width=800, height=600, tag="canvas")

dpg.setup_dearpygui()
dpg.show_viewport()
while dpg.is_dearpygui_running():
    print(resistance, is_moving)
    if is_moving:
        dpg.delete_item("canvas", children_only=True)
        for id_obj in Object.register:
            handle_phys(Object.register[id_obj])
    dpg.render_dearpygui_frame()

dpg.destroy_context()