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
        draw.circle((int(PL_CENTER[0]), int(PL_CENTER[1])), 4, fill=(255, 255, 0), width=1)
        draw.ellipse((int(PL_CENTER[0])-2, int(PL_CENTER[1])-2,int(PL_CENTER[0])+2, int(PL_CENTER[1])+2), fill=(255, 255, 0), outline="black",width=1)
        for i, el in enumerate(planets_dict):
            r = 8 * (i + 1) + 2

    w = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    m = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    seconds_absolute = time.time()
    ti = time.localtime(seconds_absolute + plusDays)
    da = ti[2]

    #draw.ellipse((158,98,162,102), fill=(255, 255, 0), outline="black",width=1)

    draw_planets(100, ti)


    
    im.save("test.png")


time.sleep(0.5)
main()
