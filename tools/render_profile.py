#!/usr/bin/python3
"""Render original profile motion and reduced-motion stills, without network."""
from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
BLUE, GREEN, TEXT, MUTED, PANEL, LINE = '#55baff', '#53e3a1', '#eef6fd', '#95afc4', '#071420', '#18364b'
FONT_ROOT = Path('/usr/share/fonts/truetype/dejavu')

def font(size, bold=False):
    return ImageFont.truetype(str(FONT_ROOT / ('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')), size)

def base(width, height):
    image = Image.new('RGB', (width, height), PANEL)
    draw = ImageDraw.Draw(image)
    for x in range(0, width, 40):draw.line((x, 0, x, height), fill='#0b1d2b', width=1)
    for y in range(0, height, 40):draw.line((0, y, width, y), fill='#0b1d2b', width=1)
    draw.rounded_rectangle((1, 1, width-2, height-2), 22, outline=LINE, width=2)
    return image, draw

def dot(draw, x, y, radius=4, color=GREEN):
    draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=color)

def hero(t):
    image, draw = base(1200, 370)
    draw.text((48, 32), 'KALEAB TAYE / SOFTWARE ENGINEER', fill=GREEN, font=font(17, True))
    draw.text((44, 85), 'Ideas into', fill=TEXT, font=font(63, True))
    draw.text((44, 159), 'experiences.', fill=BLUE, font=font(63, True))
    draw.text((48, 260), 'Code. Product. Business value.', fill=MUTED, font=font(23))
    draw.text((48, 321), 'ADDIS ABABA  /  FULL-STACK ENGINEERING', fill=MUTED, font=font(14))
    cx, cy = 963, 184
    for radius in [67, 103, 139]:draw.ellipse((cx-radius, cy-radius, cx+radius, cy+radius), outline=LINE, width=2)
    for i in range(48):
        a = i*math.tau/48
        dot(draw, cx+math.cos(a)*139, cy+math.sin(a)*139, 1.7, '#416277')
    for i, radius in enumerate([67, 103, 139]):
        angle = t*math.tau*(1 if i%2 == 0 else -1)+i*1.4
        dot(draw, cx+math.cos(angle)*radius, cy+math.sin(angle)*radius, 5, BLUE if i%2 else GREEN)
    for a in [0, math.tau/3, 2*math.tau/3]:
        x, y = cx+math.cos(a)*103, cy+math.sin(a)*103
        draw.line((cx, cy, x, y), fill='#21485c', width=2)
    draw.rounded_rectangle((cx-42, cy-32, cx+42, cy+32), 14, fill='#102c3c', outline=BLUE, width=2)
    draw.text((cx-30, cy-17), '</>', fill=GREEN, font=font(28, True))
    return image

def workflow(t):
    image, draw = base(1200, 240)
    draw.text((40, 28), 'FROM A QUESTION TO A WORKING SYSTEM', fill=MUTED, font=font(17, True))
    points = [(110, 127), (432, 127), (754, 127), (1076, 127)]
    for i in range(3):
        x, y = points[i];x2, y2 = points[i+1]
        draw.line((x+31, y, x2-31, y2), fill=LINE, width=4)
        p = (t+i/3)%1
        dot(draw, x+32+(x2-x-64)*p, y, 5, BLUE if i%2 else GREEN)
    for i, ((x, y), label) in enumerate(zip(points, ['Discover', 'Design', 'Build', 'Deliver'])):
        draw.ellipse((x-29, y-29, x+29, y+29), fill='#103043', outline=BLUE if i%2 else GREEN, width=2)
        draw.text((x-8, y-14), str(i+1), fill=TEXT, font=font(22, True))
        box = draw.textbbox((0, 0), label, font=font(23, True))
        draw.text((x-(box[2]-box[0])/2, 177), label, fill=TEXT, font=font(23, True))
    return image

def systems(t):
    image, draw = base(1200, 260)
    draw.text((40, 30), 'DIFFERENT TOOLS.', fill=TEXT, font=font(31, True))
    draw.text((40, 78), 'ONE CONNECTED EXPERIENCE.', fill=GREEN, font=font(27, True))
    draw.text((40, 148), 'Interfaces, services, data and delivery.', fill=MUTED, font=font(20))
    draw.text((40, 188), 'Designed around the product and the people using it.', fill=MUTED, font=font(15))
    points = [(800, 58), (1045, 58), (1130, 135), (1045, 213), (800, 213), (712, 135)]
    labels = ['UI', 'API', 'DATA', 'DELIVERY', 'AUTOMATION', 'PRODUCT']
    for i, (x, y) in enumerate(points):
        x2, y2 = points[(i+1)%len(points)];draw.line((x, y, x2, y2), fill=LINE, width=2)
        p = (t+i/6)%1;dot(draw, x+(x2-x)*p, y+(y2-y)*p, 4, BLUE if i%2 else GREEN)
    for i, ((x, y), label) in enumerate(zip(points, labels)):
        f = font(13, True);box = draw.textbbox((0, 0), label, font=f);half = max(30, (box[2]-box[0])/2+12)
        draw.rounded_rectangle((x-half, y-18, x+half, y+18), 10, fill='#103043', outline=BLUE if i%2 else GREEN, width=1)
        draw.text((x-(box[2]-box[0])/2, y-8), label, fill=TEXT, font=f)
    return image

def save(name, render):
    frames = [render(i/48) for i in range(48)]
    frames[0].save(ASSETS / (name+'-static.png'), optimize=True)
    pal = frames[0].quantize(colors=96)
    frames = [im.quantize(palette=pal, dither=Image.Dither.NONE) for im in frames]
    frames[0].save(ASSETS / (name+'.gif'), save_all=True, append_images=frames[1:], duration=100,
                   loop=0, optimize=True, disposal=1)

if __name__ == '__main__':
    ASSETS.mkdir(exist_ok=True)
    for name, render in [('hero', hero), ('workflow', workflow), ('systems', systems)]:
        save(name, render);print(name, (ASSETS / (name+'.gif')).stat().st_size)
