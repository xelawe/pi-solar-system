from random import getrandbits, uniform
import math
#from micropython import const


class Pluto:
    MAX_TIME = 2000
    R = 3
    BOUNCE = 0.98

    def __init__(self, imgdraw):
        self.imgdraw = imgdraw
        self.x = 240.0
        self.y = 0
        self.vel_x = -3.0
        self.y_max = 135 - Pluto.R
        self.x_min = 140 + Pluto.R
        self.x_max = 240 - Pluto.R

    def step(self, seconds, diff):
        if diff > 1000:
            diff = 1000
        invertedSeconds = 60 - seconds
        time = (invertedSeconds * 1000 - diff)
        amplitude = time / 60_000.0
        x_fun = time % Pluto.MAX_TIME / float(Pluto.MAX_TIME)
        sway = 1 - (math.pow(((x_fun / 0.5) - 1), 2) * (-1) + 1)
        add = (self.y_max - (self.y_max * amplitude))
        self.y = ((self.y_max * amplitude) * sway) + add

        self.x += self.vel_x
        if self.x >= self.x_max:
            self.vel_x *= -Pluto.BOUNCE
            self.x = self.x_max
        elif self.x <= self.x_min:
            self.vel_x *= -Pluto.BOUNCE
            self.x = self.x_min

    def draw(self):
        #self.display.set_pen(self.display.create_pen(156, 166, 183))
        #self.display.circle(int(self.x), int(self.y), Pluto.R)
        self.imgdraw.ellipse((int(self.x)-Pluto.R, int(self.y)-Pluto.R,int(self.x)+Pluto.R, int(self.y)+Pluto.R), fill=(156, 166, 183), outline=(255, 255, 0),width=1)


    def reset(self):
        vel = uniform(3, 7)
        if bool(getrandbits(1)):
            vel *= -1
        self.vel_x = vel
