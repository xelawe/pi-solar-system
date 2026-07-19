#from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_RGB565
#from pimoroni import Button, RGBLED
import time
import math
import gc
import argparse
#import machine
#from micropython import const
#import from PIL 
from PIL import Image, ImageDraw, ImageFont

# Breite/Höhe können als Kommandozeilen-Parameter übergeben werden,
# z.B. python3 main.py --width 240 --height 135
# Ohne Parameter greifen die Default-Werte (134x134).
parser = argparse.ArgumentParser(description="Pi Solar System")
parser.add_argument("--width", type=int, default=134, help="Bildbreite in Pixeln (Default: 134)")
parser.add_argument("--height", type=int, default=134, help="Bildhöhe in Pixeln (Default: 134)")
args, _ = parser.parse_known_args()

WIDTH  = args.width
HEIGHT = args.height
img_background_col = (255,255,255) #(0,0,0)
im = Image.new(mode="RGB", size=(WIDTH, HEIGHT), color=img_background_col)

draw = ImageDraw.Draw(im)

plusDays = 0

# Referenzgröße, für die die Planeten-Sprites in planets.py ursprünglich
# entworfen wurden (bei HEIGHT=134 entspricht scale = 1.0, unverändertes Original-Verhalten)
BASE_SIZE = 134

def main(datetime=1):
    global change
    import planets
    from pluto import Pluto

    # parser = argparse.ArgumentParser("pi solar system")

    def draw_planets(HEIGHT, ti):
        scale = HEIGHT / BASE_SIZE
        PL_CENTER = (int(HEIGHT / 2), int(HEIGHT / 2))
        planets_dict = planets.coordinates(ti[0], ti[1], ti[2], ti[3], ti[4])
        # draw sun in Center
        sun_radius = max(1, round(4 * scale))
        draw.ellipse((int(PL_CENTER[0])-sun_radius, int(PL_CENTER[1])-sun_radius,int(PL_CENTER[0])+sun_radius, int(PL_CENTER[1])+sun_radius), fill=(255, 255, 0), outline=(255, 255, 0),width=1)
        for i, el in enumerate(planets_dict):
            r = int((HEIGHT/2)/9) * (i + 1) + 2
            draw.ellipse((int(PL_CENTER[0])-r, int(PL_CENTER[1])-r,int(PL_CENTER[0])+r, int(PL_CENTER[1])+r), fill=None, outline=(40, 40, 40),width=1)
            feta = math.atan2(el[0], el[1])
            coordinates = (r * math.sin(feta), r * math.cos(feta))
            coordinates = (coordinates[0] + PL_CENTER[0], HEIGHT - (coordinates[1] + PL_CENTER[1]))
            # Jedes Sprite-"Pixel" wird als Rechteck gezeichnet, dessen Kanten direkt aus
            # den Grenzen der skalierten Rasterzelle berechnet werden. So schließen benachbarte
            # Rechtecke immer lückenlos aneinander an, unabhängig davon, ob "scale" eine
            # Ganzzahl ist oder nicht (verhindert das Gitter-/Karo-Muster bei krummen Skalierungen).
            for ar in range(0, len(planets.planets_a[i][0]), 5):
                px = planets.planets_a[i][0][ar] - 50
                py = planets.planets_a[i][0][ar + 1] - 50
                gx0 = coordinates[0] + px * scale
                gy0 = coordinates[1] + py * scale
                if gx0 >= 0 and gy0 >= 0:
                    gx1 = coordinates[0] + (px + 1) * scale
                    gy1 = coordinates[1] + (py + 1) * scale
                    x0 = int(math.floor(gx0))
                    y0 = int(math.floor(gy0))
                    x1 = max(x0, int(math.floor(gx1)) - 1)
                    y1 = max(y0, int(math.floor(gy1)) - 1)
                    color = (planets.planets_a[i][0][ar + 2], planets.planets_a[i][0][ar + 3], planets.planets_a[i][0][ar + 4])
                    draw.rectangle((x0, y0, x1, y1), fill=color)

    def draw_date_time(ti):
        w = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        m = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        da = ti[2]
    
        #font = ImageFont.truetype("sans-serif.ttf", 16)
        font = ImageFont.load_default()
        draw.text(( 132, 7),"%02d %s %d " % (ti[2], m[ti[1] - 1], ti[0]),fill=(244, 170, 30),font=font)
        draw.text(( 135, 93),w[ti[6]], fill=(65, 129, 50),font=font)
        draw.text(( 132, 105),"%02d:%02d" % (ti[3], ti[4]), fill=(130, 255, 100),font=font)

    mi = -1
    
    seconds_absolute = time.time()
    ti = time.localtime(seconds_absolute + plusDays)
    
    draw_planets(HEIGHT, ti)

    if (datetime == 1):
        pl = Pluto(draw)
        pl.step(ti[5], 0)
        pl.draw()

        draw_date_time(ti)

    im.save("pisolar.png")


time.sleep(0.5)
main()
