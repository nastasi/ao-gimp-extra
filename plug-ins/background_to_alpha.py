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
        

def background_to_alpha(timg, tdrw, fg_col, bg_col):
    if np is None:
        gimp.message('To calculate a geometric coefficient numpy python package is required')
        return

    if bg_col == fg_col:
        bg_col = gimp.get_background()
        fg_col = gimp.get_foreground()

    bg_pt = np.array([bg_col.r, bg_col.g, bg_col.b])
    fg_pt = np.array([fg_col.r, fg_col.g, fg_col.b])

    timg.undo_group_start()

    w = tdrw.width
    h = tdrw.height

    layer_out = pdb.gimp_layer_new(timg, w, h, RGBA_IMAGE, "Background to Alpha", 100, NORMAL_MODE)
    timg.insert_layer(layer_out)

    region = tdrw.get_pixel_rgn(0, 0, w, h)
    region_out = layer_out.get_pixel_rgn(0, 0, w, h)
    gimp.progress_init("Processing layer ...")
    for y in range(0, h):
        for x in range(0, w):
            pixel = array("B", region[x,y])
            pixel_out = array("B", region_out[x,y])
            pixel_pt = np.array([
                float(pixel[0]) / 255.0,
                float(pixel[1]) / 255.0,
                float(pixel[2]) / 255.0])
            alpha = point_projection(bg_pt, fg_pt, pixel_pt)
            alpha = 1.0 if alpha > 1.0 else (0.0 if alpha < 0.0 else alpha)
            pixel_out[0] = int(fg_col.r * 255.0)
            pixel_out[1] = int(fg_col.g * 255.0)
            pixel_out[2] = int(fg_col.b * 255.0)
            pixel_out[3] = int(alpha * 255.0)
            region_out[x,y] = pixel_out.tostring()
        gimp.progress_update(float(y) / float(h))
    layer_out.update(0, 0, w, h)
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
        (PF_COLOR, "foreground_color", "Foreground Color", (0.0, 0.0, 0.0)),
        (PF_COLOR, "background_color", "Background Color", (1.0, 1.0, 1.0)),
    ],
    [],
    background_to_alpha, menu="<Image>/Colors")

main()
