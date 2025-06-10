#from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_RGB565
#from pimoroni import Button, RGBLED
import time
import math
import gc
#import machine
#from micropython import const
#import from PIL 
from PIL import Image, ImageDraw

im = Image.new(mode="RGB", size=(320, 200), color=(255,255,255))

draw = ImageDraw.Draw(im)

plusDays = 0
def circle(xpos0, ypos0, rad):
    color = (40, 40, 40);
    x = rad - 1
    y = 0
    dx = 1
    dy = 1
    err = dx - (rad << 1)
    while x >= y:
        draw.point((xpos0 + x, ypos0 + y), fill=color)
        draw.point((xpos0 + y, ypos0 + x), fill=color)
        draw.point((xpos0 - y, ypos0 + x), fill=color)
        draw.point((xpos0 - x, ypos0 + y), fill=color)
        draw.point((xpos0 - x, ypos0 - y), fill=color)
        draw.point((xpos0 - y, ypos0 - x), fill=color)
        draw.point((xpos0 + y, ypos0 - x), fill=color)
        draw.point((xpos0 + x, ypos0 - y), fill=color)
        if err <= 0:
            y += 1
            err += dy
            dy += 2
        if err > 0:
            x -= 1
            dx += 2
            err += dx - (rad << 1)


def main():
    global change
    import planets
    from pluto import Pluto
    #set_time()



    def draw_planets(HEIGHT, ti):
        PL_CENTER = (68, int(HEIGHT / 2))
        planets_dict = planets.coordinates(ti[0], ti[1], ti[2], ti[3], ti[4])
        # t = time.ticks_ms()
        # display.set_pen(display.create_pen(255, 255, 0))
        # display.circle(int(PL_CENTER[0]), int(PL_CENTER[1]), 4)
        draw.circle((int(PL_CENTER[0]), int(PL_CENTER[1])), 4, fill=(255, 255, 0), width=1)

    draw.circle((160,100), 4, fill=(255, 255, 0), width=1)
    im.save("test.png")


time.sleep(0.5)
main()
