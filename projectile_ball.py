import math
import time

from tkinter import (
    Canvas,
    Tk,
    Button,
    Label,
    LEFT,
    RIGHT,
    StringVar
)

# ball
WIDTH = 800
HEIGHT = 600
BALL_SIZE = 50
BALL_POS = (30, HEIGHT - BALL_SIZE - 20)
BALL_COLOR = 'black'
SCORE_DIST_THRESH = 50

# ball starting pad
START_PAD_POS = (20, HEIGHT - 20)
START_PAD_SIZE = (70, 10)

# ball physics
V0 = 20  # m/s
THETA = 65
REFRESH_TIME = 15
CONST_ACC = 1  # m/s^2

# basket
RING_POSITION = (650, 200)
RING_SIZE = 100
POLE_POSITION = (
    RING_POSITION[0] + RING_SIZE / 2 - 8,
    RING_POSITION[1] + RING_SIZE
)
POLE_SIZE = (16, HEIGHT - RING_POSITION[1] - RING_SIZE)


def get_speed_x_y(v, theta):
    v_x = v * math.cos(theta * math.pi / 180)
    v_y = - v * math.sin(theta * math.pi / 180)
    return v_x, v_y


class Ball:
    def __init__(self, root, canvas, basket, simulation):
        self.root = root
        self.canvas = canvas
        self.basket = basket
        self.simulation = simulation

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
        self.reset()

    def sim_start(self, event):
        self.active = True
        self.move_active()

    def check_inside_basket(self):
        ball_pos = self.canvas.coords(self.shape)
        ring_pos = self.canvas.coords(self.basket.ring)

        inside_x = False
        inside_y = False
        if (ball_pos[0] > ring_pos[0]) and (
                ball_pos[2] < ring_pos[2]):
            inside_x = True
        if (ball_pos[1] > ring_pos[1]) and (
                ball_pos[3] < ring_pos[3]):
            inside_y = True

        return inside_x and inside_y

    def reset(self):
        current_vo = self.simulation.starting_vel
        current_theta = self.simulation.starting_theta
        self.speed_x, self.speed_y = get_speed_x_y(current_vo, current_theta)
        self.speed_init_x = self.speed_x
        self.speed_init_y = self.speed_y
        self.time = 0
        self.active = False

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
        # if pos[1] <= 0:
        #     self.reset()
        if pos[3] >= HEIGHT:
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


class Controllers:
    def __init__(self, root, simulation):
        # velocity controllers
        self.vel_plus = Button(
            root, text="vel +",
            command=simulation.increase_velocity
        )
        self.vel_minus = Button(
            root, text="vel -",
            command=simulation.decrease_velocity
        )

        self.vel_text = StringVar()
        self.vel_text.set(simulation._starting_vel)
        self.vel_display = Label(root, textvariable=self.vel_text)

        self.vel_plus.pack(side=LEFT)
        self.vel_minus.pack(side=LEFT)
        self.vel_display.pack(side=LEFT)

        # theta controllers
        self.theta_plus = Button(
            root, text="theta +",
            command=simulation.increase_theta
        )
        self.theta_minus = Button(
            root, text="theta -",
            command=simulation.decrease_theta
        )

        self.theta_text = StringVar()
        self.theta_text.set(simulation._starting_theta)
        self.theta_display = Label(root, textvariable=self.theta_text)

        self.theta_plus.pack(side=RIGHT)
        self.theta_minus.pack(side=RIGHT)
        self.theta_display.pack(side=RIGHT)


class Simulation:
    def increase_velocity(self):
        self._starting_vel += 1
        self.controllers.vel_text.set(self._starting_vel)
        self.ball.reset()

    def decrease_velocity(self):
        self._starting_vel -= 1
        self.controllers.vel_text.set(self._starting_vel)
        self.ball.reset()

    def increase_theta(self):
        self._starting_theta += 1
        self.controllers.theta_text.set(self._starting_theta)
        self.ball.reset()

    def decrease_theta(self):
        self._starting_theta -= 1
        self.controllers.theta_text.set(self._starting_theta)
        self.ball.reset()

    @property
    def starting_vel(self):
        return self._starting_vel

    @property
    def starting_theta(self):
        return self._starting_theta

    def __init__(self):
        self.root = Tk()
        self.canvas = Canvas(self.root, width=WIDTH, height=HEIGHT, bg="grey")
        self.canvas.pack()

        self._starting_vel = V0
        self._starting_theta = THETA

        # make geometries
        self.basket = Basket(self.canvas)
        self.ball = Ball(self.root, self.canvas, self.basket, self)

        # make controllers
        self.controllers = Controllers(self.root, self)

        self.root.bind("<space>", self.ball.sim_start)
        self.root.mainloop()


sim = Simulation()
