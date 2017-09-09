#!/usr/bin/env python
# Hello World in GIMP Python

from gimpfu import *
from array import array

try:
    import numpy as np
except ImportError:
    np = None

def point_projection(a, b, p):
    ap = p - a
    ab = b - a
    result = np.dot(ap, ab) / np.dot(ab, ab)
    return result
        

def background_to_alpha(timg, tdrw, bg_col, fg_col) :
    if np is None:
        gimp.message('To calculate a geometric coefficient numpy python package is required')
        return

    if tdrw.type != RGBA_IMAGE:
        gimp.message('Active layer must be of RGBA type')
        return

    if bg_col == fg_col:
        bg_col = gimp.get_background()
        fg_col = gimp.get_foreground()

    bg_pt = np.array([bg_col.r, bg_col.g, bg_col.b])
    fg_pt = np.array([fg_col.r, fg_col.g, fg_col.b])

    timg.undo_group_start()

    w = tdrw.width
    h = tdrw.height

    region = tdrw.get_pixel_rgn(0, 0, w, h)
    gimp.progress_init("Processing layer ...")
    for y in range(0, h):
        for x in range(0, w):
            pixel = array("B", region[x,y])
            # print("[%d]" % len(pixel))
            pixel_pt = np.array([
                float(pixel[0]) / 255.0,
                float(pixel[1]) / 255.0,
                float(pixel[2]) / 255.0])
            alpha = point_projection(bg_pt, fg_pt, pixel_pt)
            alpha = 1.0 if alpha > 1.0 else (0.0 if alpha < 0.0 else alpha)
            pixel[3] = int(alpha * 255.0)
            region[x,y] = pixel.tostring()
        gimp.progress_update(float(y) / float(h))
    tdrw.update(0, 0, w, h)
    gimp.progress_update(1.0)

    timg.undo_group_end()

register(
    "python_fu_background_to_alpha",
    "From background to alpha\nNOTE: if colors are the same\ncurrent fg/bg palette colors are used.",
    "Transform ",
    "Matteo Nastasi",
    "Matteo Nastasi",
    "2017",
    "Background To _Alpha...",
    "RGB*",
    [
        (PF_IMAGE, "image",       "Input image", None),
        (PF_DRAWABLE, "drawable", "Input drawable", None),
        (PF_COLOR, "background_color", "Background Color", (0.0, 0.0, 0.0)),
        (PF_COLOR, "foreground_color", "Foreground Color", (0.0, 0.0, 0.0)),
    ],
    [],
    background_to_alpha, menu="<Image>/Colors")

main()
