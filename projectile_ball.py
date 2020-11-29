import math
import time

from tkinter import (
    Canvas,
    Tk,
)

# ball
WIDTH = 800
HEIGHT = 500
BALL_POS = (30, 430)
BALL_SIZE = 50
BALL_COLOR = 'black'
SCORE_DIST_THRESH = 50

# ball starting pad
START_PAD_POS = (20, HEIGHT - 20)
START_PAD_SIZE = (70, 10)

# ball physics
V0 = 30  # m/s
THETA = 45
REFRESH_TIME = 15
CONST_ACC = 1  # m/s^2

# basket
RING_POSITION = (650, 200)
RING_SIZE = 100
POLE_POSITION = (
    RING_POSITION[0] + RING_SIZE / 2 - 8,
    RING_POSITION[1] + RING_SIZE
)
POLE_SIZE = (16, 200)


def get_speed_x_y(v, theta):
    v_x = v * math.cos(theta * math.pi / 180)
    v_y = - v * math.sin(theta * math.pi / 180)
    return v_x, v_y


class Ball:
    def __init__(self, root, canvas, basket):
        self.root = root
        self.canvas = canvas
        self.basket = basket

        self.shape = self.canvas.create_oval(
            BALL_POS[0], BALL_POS[1],
            BALL_POS[0] + BALL_SIZE,
            BALL_POS[1] + BALL_SIZE, fill=BALL_COLOR
        )
        self.pad = canvas.create_rectangle(
            START_PAD_POS[0], START_PAD_POS[1],
            START_PAD_POS[0] + START_PAD_SIZE[0],
            START_PAD_POS[1] + START_PAD_SIZE[1],
        )
        self.speed_x, self.speed_y = get_speed_x_y(V0, THETA)
        self.speed_init_x = self.speed_x
        self.speed_init_y = self.speed_y
        self.time = 0
        self.active = False

    def sim_start(self, event):
        self.active = True
        self.move_active()

    def check_inside_basket(self):
        ball_pos = self.canvas.coords(self.shape)
        ring_pos = self.canvas.coords(self.basket.ring)

        inside_x = False
        inside_y = False
        if (ball_pos[0] > ring_pos[0]) and (
                ball_pos[0] + BALL_SIZE < ring_pos[0] + RING_SIZE):
            inside_x = True
        if (ball_pos[1] > ring_pos[1]) and (
                ball_pos[1] + BALL_SIZE < ring_pos[1] + RING_SIZE):
            inside_y = True

        return inside_x and inside_y

    def reset(self):
        self.active = False
        self.speed_x, self.speed_y = get_speed_x_y(V0, THETA)
        self.time = 0

        # move ball to start
        ball_pos_now = self.canvas.coords(self.shape)
        pos_diff = (
            BALL_POS[0] - ball_pos_now[0],
            BALL_POS[1] - ball_pos_now[1],
        )
        self.canvas.move(self.shape, pos_diff[0], pos_diff[1])

    def ball_projectile(self):
        self.canvas.move(self.shape, self.speed_x, self.speed_y)
        self.time += 1

        self.speed_y = self.speed_init_y + self.time * CONST_ACC

        if self.check_inside_basket():
            print('yay scored')

        pos = self.canvas.coords(self.shape)
        if pos[2] >= WIDTH or pos[0] <= 0:
            self.reset()
        if pos[3] >= HEIGHT or pos[1] <= 0:
            self.reset()

    def move_active(self):
        if self.active:
            # self.ball_update()
            self.ball_projectile()
            self.root.after(REFRESH_TIME, self.move_active)


class Basket:
    def __init__(self, canvas):
        self.canvas = canvas
        self.ring = self.canvas.create_oval(
            RING_POSITION[0], RING_POSITION[1],
            RING_POSITION[0] + RING_SIZE,
            RING_POSITION[1] + RING_SIZE, outline='blue'
        )
        self.pole = self.canvas.create_rectangle(
            POLE_POSITION[0], POLE_POSITION[1],
            POLE_POSITION[0] + POLE_SIZE[0],
            POLE_POSITION[1] + POLE_SIZE[1], outline='blue'
        )


class Simulation:
    def __init__(self):
        self.root = Tk()
        self.canvas = Canvas(self.root, width=WIDTH, height=HEIGHT, bg="grey")
        self.canvas.pack()

        self.basket = Basket(self.canvas)
        self.ball = Ball(self.root, self.canvas, self.basket)

        self.root.bind("<space>", self.ball.sim_start)

        self.root.mainloop()


sim = Simulation()
