#from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_RGB565
#from pimoroni import Button, RGBLED
import time
import math
import gc
#import machine
#from micropython import const
#import from PIL 
from PIL import Image, ImageDraw, ImageFont

HEIGHT = 134
WIDTH  = 240
im = Image.new(mode="RGB", size=(WIDTH, HEIGHT), color=(255,255,255))

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
        # draw sun in Center
        draw.ellipse((int(PL_CENTER[0])-2, int(PL_CENTER[1])-2,int(PL_CENTER[0])+2, int(PL_CENTER[1])+2), fill=(255, 255, 0), outline=(255, 255, 0),width=1)
        for i, el in enumerate(planets_dict):
            r = 8 * (i + 1) + 2
            #display.set_pen(display.create_pen(40, 40, 40))
            circle(PL_CENTER[0], PL_CENTER[1], r)
            feta = math.atan2(el[0], el[1])
            coordinates = (r * math.sin(feta), r * math.cos(feta))
            coordinates = (coordinates[0] + PL_CENTER[0], HEIGHT - (coordinates[1] + PL_CENTER[1]))
            for ar in range(0, len(planets.planets_a[i][0]), 5):
                x = planets.planets_a[i][0][ar] - 50 + coordinates[0]
                y = planets.planets_a[i][0][ar + 1] - 50 + coordinates[1]
                if x >= 0 and y >= 0:
                    draw.point((int(x), int(y)), fill=(planets.planets_a[i][0][ar + 2], planets.planets_a[i][0][ar + 3], planets.planets_a[i][0][ar + 4]))

    def draw_date_time(ti):
        w = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        m = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        da = ti[2]
    
        #font = ImageFont.truetype("sans-serif.ttf", 16)
        font = ImageFont.load_default()
        draw.text(( 132, 7),"%02d %s %d " % (ti[2], m[ti[1] - 1], ti[0]),fill=(244, 170, 30),font=font)
        draw.text(( 135, 93),w[ti[6]], fill=(65, 129, 50),font=font)
        draw.text(( 132, 105),"%02d:%02d" % (ti[3], ti[4]), fill=(130, 255, 100),font=font)

    
    seconds_absolute = time.time()
    ti = time.localtime(seconds_absolute + plusDays)
    
    draw_planets(HEIGHT, ti)

    draw_date_time(ti)

    im.save("planets.png")


time.sleep(0.5)
main()
