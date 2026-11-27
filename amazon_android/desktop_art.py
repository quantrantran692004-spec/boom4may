"""Local vector-style artwork for the ice/glass desktop presentation.

All images are drawn locally from geometry; no app data is used in the artwork.
"""
from functools import lru_cache
import math
from PIL import Image, ImageDraw, ImageFilter, ImageColor


def gradient(size, stops, horizontal=False):
    w, h = size
    image = Image.new("RGBA", size)
    draw = ImageDraw.Draw(image)
    length = w if horizontal else h
    colors = [(at, ImageColor.getrgb(color)) for at, color in stops]
    for i in range(length):
        t = i / max(1, length - 1)
        a, b = colors[0], colors[-1]
        for left, right in zip(colors, colors[1:]):
            if left[0] <= t <= right[0]:
                a, b = left, right
                break
        mix = max(0, min(1, (t - a[0]) / max(.0001, b[0] - a[0])))
        color = tuple(round(x + (y - x) * mix) for x, y in zip(a[1], b[1]))
        draw.line((i, 0, i, h) if horizontal else (0, i, w, i), fill=color)
    return image


@lru_cache(maxsize=128)
def rounded_surface(width, height, role="panel", selected=False, color="#F5FAFE"):
    w, h = max(8, width), max(8, height)
    image = Image.new("RGBA", (w, h))
    radius = min(24, h / 3)
    shadow = Image.new("RGBA", (w, h))
    ImageDraw.Draw(shadow).rounded_rectangle((4, 7, w - 4, h - 2), radius,
                                           fill=(28, 97, 139, 45))
    image.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(4)))
    stops = [(0, "#FFFFFF"), (.5, "#F5FAFE"), (1, "#EAF6FD")]
    if selected:
        stops = [(0, "#F2FDFF"), (.5, "#E9F6FF"), (1, "#D9F6FF")]
    mask = Image.new("L", (w, h))
    ImageDraw.Draw(mask).rounded_rectangle((3, 2, w-4, h-7), radius, fill=255)
    face = Image.new("RGBA", (w, h), color)
    face.putalpha(mask)
    image.alpha_composite(face)
    d = ImageDraw.Draw(image)
    d.rounded_rectangle((3, 2, w-4, h-7), radius,
                        outline="#12BFFF" if selected else "#C5DFEE", width=2 if selected else 1)
    d.rounded_rectangle((5, 4, w-6, h-9), max(1, radius-2), outline="#FFFFFF", width=1)
    return image


@lru_cache(maxsize=128)
def button_face(width, height, role, disabled=False, hover=False):
    palettes = {
        "primary": ("#30C7FF", "#0874F3", "#003DD2", "#A0FAFF"),
        "batch-stop": ("#FF969D", "#F83A51", "#D71936", "#FFE5E8"),
        "clipboard": ("#23D6BC", "#078A9D", "#005777", "#A5F7EF"),
        "stop": ("#FFFFFF", "#FFF3F6", "#F9DFE8", "#FF9CB0"),
        "danger": ("#FFFFFF", "#FFF0F5", "#F8DCE6", "#FFA1B9"),
        "continue": ("#FFFFFF", "#F1FBFF", "#C8EFFF", "#6BACFF"),
        "secondary": ("#FFFFFF", "#F6FBFE", "#DEEDF6", "#C1E6F3"),
        "settings": ("#FFFFFF", "#F7FCFF", "#E0F1FB", "#FFFFFF"),
        "fill": ("#EFFCFE", "#E1F2F6", "#C9E7ED", "#B0DEE8"),
    }
    top, mid, bottom, edge = palettes.get(role, palettes["secondary"])
    if disabled:
        top, mid, bottom, edge = "#F5F9FC", "#EAF1F6", "#DCE8EF", "#C6D8E3"
    if hover and not disabled:
        top, mid = mid, top
    w, h = max(8, width), max(8, height)
    im = Image.new("RGBA", (w, h))
    shadow = Image.new("RGBA", (w, h))
    d = ImageDraw.Draw(shadow)
    radius = min(17, h*.26)
    d.rounded_rectangle((3, 5, w-3, h-1), radius, fill=(14, 85, 128, 65))
    im.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(3)))
    mask = Image.new("L", (w, h))
    ImageDraw.Draw(mask).rounded_rectangle((2, 1, w-3, h-5), radius, fill=255)
    face = gradient((w, h), [(0, top), (.48, mid), (1, bottom)])
    face.putalpha(mask)
    im.alpha_composite(face)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((2, 1, w-3, h-5), radius, outline=edge, width=2)
    d.rounded_rectangle((4, 3, w-5, h-7), max(2, radius-2), outline=(255,255,255,190), width=1)
    return im


def bezier(points, steps=160):
    p0,p1,p2,p3=points
    return [tuple((1-t)**3*p0[j]+3*(1-t)**2*t*p1[j]+3*(1-t)*t*t*p2[j]+t**3*p3[j]
                  for j in (0,1)) for t in (i/steps for i in range(steps+1))]


@lru_cache(maxsize=24)
def banner(width, height, footer=False):
    im = gradient((width,height), [(0,"#99E6EF"),(.45,"#43B5C9"),(.78,"#005466"),(1,"#005466")]
                  if footer else [(0,"#DFEFF9"),(.55,"#DDF3FC"),(1,"#D9F3FC")], True)
    layer=Image.new("RGBA", im.size)
    if footer:
        width = round(width*.78)
    d=ImageDraw.Draw(layer)
    top = bezier([(width*.43,height*1.02),(width*.66,-height*1.1),
                  (width*.72,height*2.0),(width*.92,-height*.4)])
    bottom = bezier([(width*.43,height*1.25),(width*.67,-height*.55),
                     (width*.79,height*2.6),(width*1.02,-height*.65)])
    ribbon_mask = Image.new("L", im.size)
    ImageDraw.Draw(ribbon_mask).polygon(top + list(reversed(bottom)), fill=220)
    ribbon = gradient(im.size, [(0,"#BAF6F5"),(.55,"#68DFEA"),(.7,"#009CAE"),(.9,"#16CFB9"),(1,"#ACFBF3")], True)
    ribbon.putalpha(ribbon_mask)
    layer.alpha_composite(ribbon)
    d=ImageDraw.Draw(layer)
    for i in range(34):
        offset=i/34
        points=bezier([(width*.43,height*(1.02-offset*.22)),
                      (width*.67,-height*(1.1+offset*.2)),
                      (width*.69,height*(2.0-offset*.5)),
                      (width*(.91+offset*.09),-height*.4)])
        d.line(points,fill=(9,187+round(offset*45),199,round(20+offset*25)),width=max(2,round(height*.08)))
    for i in range(4):
        p=bezier([(width*.49,height*(.75+i*.04)),(width*.68,-height*.92),
                  (width*.73,height*2.1),(width*(.96+i*.014),-height*.35)])
        d.line(p,fill=(226,255,255,210-i*35),width=1)
    im.alpha_composite(layer)
    if footer:
        width=im.width
        mask=Image.new("L",im.size)
        ImageDraw.Draw(mask).rounded_rectangle((1,1,width-2,height-2),28,fill=255)
        im.putalpha(mask)
        ImageDraw.Draw(im).rounded_rectangle((2,2,width-3,height-3),27,outline="#F3FFFF",width=2)
    return im


@lru_cache(maxsize=12)
def phone_art(variant=0):
    w,h=156,240
    im=Image.new("RGBA",(w,h))
    sh=Image.new("RGBA",im.size)
    ImageDraw.Draw(sh).rounded_rectangle((25,17,132,227),23,fill=(0,99,132,90))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(9)))
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((20,10,130,224),22,fill="#011A2C",outline="#A7D8E2",width=3)
    d.rounded_rectangle((25,15,125,219),18,fill="#040F22",outline="#54798D",width=2)
    palettes=[("#51E8F5","#0E49D2","#EAABF7"),("#85FFCF","#04A697","#AAECFD"),("#C38AFF","#4827B7","#F0B3ED")]
    top,mid,bottom=palettes[variant%3]
    screen=gradient((94,198),[(0,top),(.45,mid),(1,bottom)])
    sheen=Image.new("RGBA",screen.size)
    sd=ImageDraw.Draw(sheen)
    sd.polygon([(0,0),(35,0),(94,145),(94,198),(45,198),(0,98)],fill=(198,249,255,55))
    for pts in [[(0,0),(0,90),(94,76),(94,198)],[(0,185),(9,125),(94,119),(94,24)]]:
        sd.line(bezier(pts),fill=(232,255,255,180),width=2)
    screen.alpha_composite(sheen)
    mask=Image.new("L",screen.size)
    ImageDraw.Draw(mask).rounded_rectangle((0,0,93,197),14,fill=255)
    screen.putalpha(mask)
    im.alpha_composite(screen,(29,20))
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((59,22,91,26),3,fill=(0,17,43,120))
    d.line((132,55,132,88),fill="#326375",width=3)
    return im


@lru_cache(maxsize=1)
def brand_art():
    im=button_face(128,128,"clipboard")
    d=ImageDraw.Draw(im)
    for y in (66,53,40):
        d.line([(34,y+8),(64,y+24),(94,y+8)],fill="white",width=7,joint="curve")
    d.polygon([(34,44),(64,27),(94,44),(64,61)],fill="white")
    return im
