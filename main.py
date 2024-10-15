from graphics_template import *
from tkinter import Tk, Canvas
import time
import numpy as np

simulation_done = False
DELTA_TDRAW = 0.02
DELTA_TSIM = 0.0005

vp_width, vp_height = 1024, 768
w_xmin, w_ymin, w_xmax = -5, -3, 5
w_ymax = w_ymin + (w_xmax - w_xmin) / vp_width * vp_height

CEILING = w_ymax - 0.5
FLOOR = w_ymin + 0.5

pos_x = 0
pos_y = 0
prev_y = 0

k = 30  # N/m
m = 1  # kg
g = 9.81  # m/(s*s)

AMOUNT = 10


def init_positions(n):
    return np.linspace(-2, 4, n)


def draw_positions():
    YELLOW = rgb_col(255, 255, 0)
    RED = rgb_col(255, 0, 0)
    for i in pos_y2:
        draw_dot(canvas, 0, i, RED)
        draw_line(canvas, 0, CEILING, 0, i, YELLOW)


def left_click(event):
    global simulation_done
    simulation_done = True


def draw_scene():
    RED = rgb_col(255, 0, 0)
    GREEN = rgb_col(0, 255, 0)
    draw_line(canvas, w_xmin, FLOOR, w_xmax, FLOOR, RED)  # FLOOR
    draw_line(canvas, w_xmin / 2, CEILING, w_xmax / 2, CEILING, GREEN)  # CEILING
    draw_dot(canvas, pos_x, pos_y, RED)


def do_simulation():
    global pos_y, prev_y
    dt = DELTA_TSIM

    if CEILING > pos_y > FLOOR:
        a = -g - (k * pos_y) / m
        tmp_y = pos_y
        pos_y = 2 * pos_y - prev_y + a * dt * dt
        prev_y = tmp_y
    else:
        pos_y = 0
        prev_y = 0


window = Tk()
canvas = Canvas(window, width=vp_width, height=vp_height, bg=rgb_col(0, 0, 0))
canvas.pack()
canvas.bind("<Button-1>", left_click)

init_graphics(vp_width, vp_height, w_xmin, w_ymin, w_xmax)

init_time = time.perf_counter()
prev_draw_time = 0
prev_sim_time = 0

#pos_y2 = init_positions(10)

while not simulation_done:
    # SIMULATION
    sim_dt = time.perf_counter() - init_time - prev_sim_time
    if sim_dt > DELTA_TSIM:
        do_simulation()
        prev_sim_time += DELTA_TSIM

    # DRAWING
    draw_dt = time.perf_counter() - init_time - prev_draw_time
    if draw_dt > DELTA_TDRAW:
        canvas.delete("all")
        draw_scene()
        #draw_positions()
        canvas.update()
        prev_draw_time += DELTA_TDRAW
