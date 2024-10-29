from tkinter import Tk, Canvas
from graphics_template import *
import math, time

vp_width, vp_height = 1024, 768
w_xmin, w_ymin, w_xmax = -10, 0, 10
w_ymax = w_ymin + (w_xmax - w_xmin) / vp_width * vp_height

simulation_done = False
DELTA_TSIM = 0.0005
DELTA_TDRAW = 0.02  # 50 fps

CEILING = w_ymax - 0.5
FLOOR = w_ymin + 0.5

pos_x = 0.0
pos_y = []

AMOUNT = 2

# constanten
m = 10
g = 9.81
k = 100
l0 = 1
kd = 10


def left_click(event):
    global simulation_done
    simulation_done = True


def bereken_kracht(i, dt):
    Fzw = -m * g
    Fd = -(pos_y[i][0] - pos_y[i][1]) / (2 * dt) * kd

    if i == 0:  # eerste
        Fk1 = k * (CEILING - pos_y[i][0])  # omhoog
        fk2 = k * (pos_y[i + 1][0] - pos_y[i][0])  # omlaag
    elif i == AMOUNT - 1:  # laatste
        Fk1 = k * (pos_y[i - 1][0] - pos_y[i][0])
        fk2 = 0
    else:
        Fk1 = k * (pos_y[i - 1][0] - pos_y[i][0])
        fk2 = 0 # TODO

    return Fzw + Fk1 + fk2 + Fd


def do_simulation(dt):
    tmp1 = pos_y[0][0]
    pos_y[0][0] = 2 * pos_y[0][0] - pos_y[0][1] + (bereken_kracht(0, dt) / m) * dt * dt
    pos_y[0][1] = tmp1

    tmp2 = pos_y[1][0]
    pos_y[1][0] = 2 * pos_y[1][0] - pos_y[1][1] + (bereken_kracht(1, dt) / m) * dt * dt
    pos_y[1][1] = tmp2


def draw_scene():
    # draw_grid (canvas)
    RED = rgb_col(255, 0, 0)
    GREEN = rgb_col(0, 255, 0)
    YELLOW = rgb_col(255, 255, 0)
    draw_line(canvas, w_xmin / 2, CEILING, w_xmax / 2, CEILING, GREEN)
    for i in range(0, AMOUNT):
        draw_dot(canvas, pos_x, pos_y[i][0], YELLOW)


def init_scene():
    for i in range(1, AMOUNT + 1):
        pos_y.append([CEILING - (l0 * i), CEILING - (l0 * i)])
    draw_scene()


window = Tk()
canvas = Canvas(window, width=vp_width, height=vp_height, bg=rgb_col(0, 0, 0))
canvas.pack()
canvas.bind("<Button-1>", left_click)

init_graphics(vp_width, vp_height, w_xmin, w_ymin, w_xmax)

init_time = time.perf_counter()
prev_draw_time = 0
prev_sim_time = 0

init_scene()

while not simulation_done:
    # simulating
    sim_dt = time.perf_counter() - init_time - prev_sim_time
    if sim_dt > DELTA_TSIM:
        do_simulation(DELTA_TSIM)
        prev_sim_time += DELTA_TSIM
    # drawing
    draw_dt = time.perf_counter() - init_time - prev_draw_time
    if draw_dt > DELTA_TDRAW:  # 50 fps
        canvas.delete("all")
        draw_scene()
        canvas.update()
        prev_draw_time += DELTA_TDRAW
