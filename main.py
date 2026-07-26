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
parser.add_argument("--orbit-style", choices=["circle", "ellipse"], default="circle",
                     help="Darstellung der Planetenbahnen: 'circle' = Draufsicht (Standard), "
                          "'ellipse' = perspektivische Darstellung wie beim Casio CGW-50 Cosmo Phase")
parser.add_argument("--ellipse-ratio", type=float, default=0.45,
                     help="Vertikaler Stauchungsfaktor der Ellipsen bei --orbit-style ellipse. "
                          "1.0 = Kreis, kleinere Werte = flacher (Standard: 0.45)")
parser.add_argument("--planet-style", choices=["sprite", "circle"], default="sprite",
                     help="Darstellung der Planeten: 'sprite' = Original-Pixelgrafik (Standard), "
                          "'circle' = einfache gefüllte Kreise mit Kürzel - kontrastreicher und "
                          "eignet sich besser für Graustufen-Darstellung")
parser.add_argument("--output", type=str, default="pisolar.png",
                     help="Dateiname für das erzeugte PNG (Standard: pisolar.png)")
args, _ = parser.parse_known_args()

WIDTH  = args.width
HEIGHT = args.height
ORBIT_STYLE = args.orbit_style
PLANET_STYLE = args.planet_style
# Stauchungsfaktor auf einen sinnvollen Bereich begrenzen
ELLIPSE_RATIO = min(1.0, max(0.1, args.ellipse_ratio))

# Metadaten für den "circle"-Darstellungsmodus: Name, Kürzel (Merkur/Mars
# fangen beide mit "M" an, daher zweistellige Kürzel statt nur Anfangsbuchstabe),
# Farbe und Durchmesser (in Pixeln, bei ORBIT_SIZE=BASE_SIZE=134, skaliert mit
# 'scale' wie die Sprite-Grafiken). Reihenfolge entspricht exakt der Reihenfolge
# von planets.coordinates(): Merkur, Venus, Erde, Mars, Jupiter, Saturn, Uranus, Neptun.
PLANET_INFO = [
    {"name": "Merkur",  "label": "Me", "color": (169, 169, 169), "diameter": 5},
    {"name": "Venus",   "label": "V",  "color": (218, 165, 105), "diameter": 7},
    {"name": "Erde",    "label": "E",  "color": (70, 130, 180),  "diameter": 7},
    {"name": "Mars",    "label": "Ma", "color": (193, 68, 14),   "diameter": 6},
    {"name": "Jupiter", "label": "J",  "color": (216, 181, 137), "diameter": 11},
    {"name": "Saturn",  "label": "S",  "color": (235, 214, 168), "diameter": 10},
    {"name": "Uranus",  "label": "U",  "color": (172, 229, 238), "diameter": 8},
    {"name": "Neptun",  "label": "N",  "color": (62, 84, 178),   "diameter": 8},
]

# Referenzgröße, für die die Planeten-Sprites in planets.py ursprünglich
# entworfen wurden (bei ORBIT_SIZE=134 entspricht scale = 1.0, unverändertes Original-Verhalten)
BASE_SIZE = 134

if ORBIT_STYLE == "ellipse":
    # Im Ellipsen-Modus richten sich die Umlaufbahnen nach der Breite (WIDTH),
    # und die Bildhöhe wird automatisch so berechnet, dass sie genau zur
    # flachen Form der Ellipsen passt - ein übergebener --height Wert wird
    # dabei bewusst ignoriert, damit kein quadratischer Canvas mit viel
    # Leerraum oben/unten entsteht.
    ORBIT_SIZE = WIDTH
    scale = ORBIT_SIZE / BASE_SIZE
    outer_r = int((ORBIT_SIZE / 2) / 9) * 9 + 2
    margin = max(4, round(8 * scale))
    HEIGHT = int(outer_r * ELLIPSE_RATIO) * 2 + margin
else:
    ORBIT_SIZE = HEIGHT

img_background_col = (255,255,255) #(0,0,0)
im = Image.new(mode="RGB", size=(WIDTH, HEIGHT), color=img_background_col)

draw = ImageDraw.Draw(im)

plusDays = 0

def main(datetime=1):
    global change
    import planets
    from pluto import Pluto

    # parser = argparse.ArgumentParser("pi solar system")

    def draw_planets(HEIGHT, ti):
        scale = ORBIT_SIZE / BASE_SIZE
        PL_CENTER = (int(ORBIT_SIZE / 2), int(HEIGHT / 2))
        planets_dict = planets.coordinates(ti[0], ti[1], ti[2], ti[3], ti[4])
        # draw sun in Center
        sun_radius = max(1, round(4 * scale))
        draw.ellipse((int(PL_CENTER[0])-sun_radius, int(PL_CENTER[1])-sun_radius,int(PL_CENTER[0])+sun_radius, int(PL_CENTER[1])+sun_radius), fill=(255, 255, 0), outline=(255, 255, 0),width=1)
        for i, el in enumerate(planets_dict):
            r = int((ORBIT_SIZE/2)/9) * (i + 1) + 2
            # Vertikaler Stauchungsfaktor der Umlaufbahn: 1.0 = Kreis (Draufsicht),
            # < 1.0 = flache Ellipse (perspektivische Darstellung wie beim Cosmo Phase)
            ratio = ELLIPSE_RATIO if ORBIT_STYLE == "ellipse" else 1.0
            rv = int(r * ratio)
            draw.ellipse((int(PL_CENTER[0])-r, int(PL_CENTER[1])-rv,int(PL_CENTER[0])+r, int(PL_CENTER[1])+rv), fill=None, outline=(40, 40, 40),width=1)
            feta = math.atan2(el[0], el[1])
            coordinates = (r * math.sin(feta), r * ratio * math.cos(feta))
            coordinates = (coordinates[0] + PL_CENTER[0], HEIGHT - (coordinates[1] + PL_CENTER[1]))

            if PLANET_STYLE == "circle":
                info = PLANET_INFO[i]
                d = max(2, round(info["diameter"] * scale))
                cx, cy = coordinates
                color = info["color"]
                draw.ellipse((cx - d / 2, cy - d / 2, cx + d / 2, cy + d / 2),
                             fill=color, outline=(0, 0, 0), width=1)
                # Kontrastfarbe für das Kürzel anhand der wahrgenommenen Helligkeit
                # der Planetenfarbe wählen - das funktioniert auch nach einer
                # Umwandlung in Graustufen zuverlässig (schwarz auf hell, weiß auf dunkel).
                luminance = 0.299 * color[0] + 0.587 * color[1] + 0.114 * color[2]
                text_color = (0, 0, 0) if luminance > 140 else (255, 255, 255)
                font = ImageFont.load_default()
                label = info["label"]
                bbox = draw.textbbox((0, 0), label, font=font)
                tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
                draw.text((cx - tw / 2 - bbox[0], cy - th / 2 - bbox[1]), label, fill=text_color, font=font)
                continue

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

        if ORBIT_STYLE == "ellipse":
            # Die Bildhöhe wird im Ellipsen-Modus automatisch berechnet und ist meist
            # deutlich kleiner als das Original-Design (134px) vorsah. Nur die
            # Y-Position wird deshalb proportional zur tatsächlichen Bildhöhe skaliert,
            # damit die drei Textzeilen innerhalb des (flacheren) Bildes bleiben. Die
            # X-Position bleibt unverändert, da die Breite des (nicht skalierbaren)
            # Bitmap-Fonts konstant ist - Mitskalieren würde den Text bei größeren
            # Bildern nur weiter aus dem Canvas hinaus schieben.
            scale_y = HEIGHT / BASE_SIZE
            pos1 = (132, int(7 * scale_y))
            pos2 = (135, int(93 * scale_y))
            pos3 = (132, int(105 * scale_y))
        else:
            pos1 = (132, 7)
            pos2 = (135, 93)
            pos3 = (132, 105)

        draw.text(pos1,"%02d %s %d " % (ti[2], m[ti[1] - 1], ti[0]),fill=(244, 170, 30),font=font)
        draw.text(pos2,w[ti[6]], fill=(65, 129, 50),font=font)
        draw.text(pos3,"%02d:%02d" % (ti[3], ti[4]), fill=(130, 255, 100),font=font)

    mi = -1
    
    seconds_absolute = time.time()
    ti = time.localtime(seconds_absolute + plusDays)
    
    draw_planets(HEIGHT, ti)

    #if (datetime == 1):
    #    pl = Pluto(draw)
    #    pl.step(ti[5], 0)
    #    pl.draw()

    #    draw_date_time(ti)

    im.save(args.output)


time.sleep(0.5)
main()
