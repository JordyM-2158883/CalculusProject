from tkinter import Tk, Canvas, mainloop
from graphics_template import *
import time

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

AMOUNT = 10

# constanten
m = 1
g = 9.81
k = 100
l0 = 0.5
kd = 0.5


def left_click(event):
    global simulation_done
    simulation_done = True


def bereken_kracht(i, dt):
    Fzw = -m * g
    Fd = -(pos_y[i][0] - pos_y[i][1]) / (2 * dt) * kd

    if i == 0:  # eerste
        Fk1 = k * (CEILING - pos_y[i][0] - l0)  # omhoog
        fk2 = k * (pos_y[i + 1][0] - pos_y[i][0] + l0)  # omlaag
    elif i == AMOUNT - 1:  # laatste
        Fk1 = k * (pos_y[i - 1][0] - pos_y[i][0] - l0)
        fk2 = 0
    else:
        Fk1 = k * (pos_y[i - 1][0] - pos_y[i][0] - l0)
        fk2 = k * (pos_y[i + 1][0] - pos_y[i][0] + l0)

    return Fzw + Fk1 + fk2 + Fd


def do_simulation(dt):
    for i in range(0, AMOUNT):
        tmp = pos_y[i][0]
        pos_y[i][0] = (
            2 * pos_y[i][0] - pos_y[i][1] + (bereken_kracht(i, dt) / m) * dt * dt
        )
        pos_y[i][1] = tmp


def draw_scene():
    # draw_grid (canvas)
    RED = rgb_col(255, 0, 0)
    GREEN = rgb_col(0, 255, 0)
    YELLOW = rgb_col(255, 255, 0)
    draw_line(canvas, w_xmin / 2, CEILING, w_xmax / 2, CEILING, GREEN)
    for i in range(0, AMOUNT):
        if i == 0:
            draw_line(canvas, pos_x, CEILING, pos_x, pos_y[i][0], YELLOW)
        else:
            draw_line(canvas, pos_x, pos_y[i - 1][0], pos_x, pos_y[i][0], YELLOW)
        draw_dot(canvas, pos_x, pos_y[i][0], RED)


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

def main():
    global prev_draw_time, prev_sim_time
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

if __name__ == '__main__':
    main()
    mainloop()
