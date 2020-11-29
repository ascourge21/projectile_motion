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
SIZE = 50
BALL_COLOR = 'black'

# ball starting pad
START_PAD_POS = (20, HEIGHT - 20)
START_PAD_SIZE = (70, 10)

# basket
RING_POSITION = (650, 200)
RING_SIZE = 100
POLE_POSITION = (
    RING_POSITION[0] + RING_SIZE / 2 - 8,
    RING_POSITION[1] + RING_SIZE
)
POLE_SIZE = (16, 200)


class Ball:
    def __init__(self, root, canvas):
        self.root = root
        self.canvas = canvas
        self.shape = self.canvas.create_oval(
            BALL_POS[0], BALL_POS[1],
            BALL_POS[0] + SIZE,
            BALL_POS[1] + SIZE, fill=BALL_COLOR
        )
        self.pad = canvas.create_rectangle(
            START_PAD_POS[0], START_PAD_POS[1],
            START_PAD_POS[0] + START_PAD_SIZE[0],
            START_PAD_POS[1] + START_PAD_SIZE[1],
        )
        self.speedx = 9  # changed from 3 to 9
        self.speedy = 9  # changed from 3 to 9
        self.active = False

    def sim_start(self, event):
        self.active = True
        self.move_active()

    def ball_update(self):
        self.canvas.move(self.shape, self.speedx, self.speedy)
        pos = self.canvas.coords(self.shape)
        if pos[2] >= WIDTH or pos[0] <= 0:
            self.speedx *= -1
        if pos[3] >= HEIGHT or pos[1] <= 0:
            self.speedy *= -1

    def move_active(self):
        if self.active:
            self.ball_update()
            self.root.after(40, self.move_active) # changed from 10ms to 30ms


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

        self.ball = Ball(self.root, self.canvas)
        self.basket = Basket(self.canvas)

        print('gogo')
        self.root.bind("<space>", self.ball.sim_start)

        self.root.mainloop()


sim = Simulation()
