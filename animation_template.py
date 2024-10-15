from tkinter import Tk, Canvas
from graphics_template import *
import math, time

vp_width, vp_height = 1024, 768
w_xmin, w_ymin, w_xmax = -5, -3, 5
w_ymax = w_ymin + (w_xmax - w_xmin)/vp_width * vp_height

RADIUS = 2
obj_pos = []
animation_done = False
DELTA_TDRAW = 0.02  # 50 fps


def do_animation (t):
    global animation_done
    # animation stops after 2 rotations
    if (t > 4*math.pi):     
        animation_done = True
        t = 4*math.pi  # force state to end state
    # constant rotation around origin
    obj_pos[0] = RADIUS * math.cos(t)
    obj_pos[1] = RADIUS * math.sin(t)


def draw_scene ():
    draw_grid(canvas)
    draw_axis(canvas)
    fill_coll = rgb_col (255,0,0)
    draw_line (canvas, 0, 0, obj_pos[0], obj_pos[1], fill_coll)
    draw_dot (canvas, obj_pos[0], obj_pos[1], fill_coll)


def init_scene ():
    obj_pos.append (0.0)    # x-coord 
    obj_pos.append (0.0)    # y-coord
    # dummy values, set in do_animation (0.0)
    do_animation (0.0)
    draw_scene ()


window = Tk()
canvas = Canvas(window, width=vp_width, height=vp_height, bg=rgb_col(0,0,0))
canvas.pack()

init_graphics (vp_width, vp_height, w_xmin, w_ymin, w_xmax)

# time.perf_counter() -> float. Return the value (in fractional seconds)
# of a performance counter, i.e. a clock with the highest available resolution
# to measure a short duration. It does include time elapsed during sleep and
# is system-wide. The reference point of the returned value is undefined,
# so that only the difference between the results of consecutive calls is valid.

init_time = time.perf_counter()
prev_draw_time = 0
init_scene ()

while (not animation_done):
    draw_dt = time.perf_counter() - init_time - prev_draw_time
    if (draw_dt > DELTA_TDRAW): # 50 fps
        prev_draw_time += DELTA_TDRAW
        do_animation (prev_draw_time)
        canvas.delete("all")
        draw_scene()
        canvas.update()

