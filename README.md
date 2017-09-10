# AlternativeOutput Extra Gimp features

## Plugin - Background to alpha

### Description

Starting from a  layer with mainly 2 colors or a mix of them create an alpha channel
using in the 3D space of color the intersection between the segment between foregrond
and background color points and the perpendiculare plane passing by each pixel of
the layer.

### Usage

In a layer with mainly 2 colors or a mix of them

![](./img/b2a_example0.png "")

from **"Colors"** menu run **"Background to Alpha ..."** plugin
![](./img/b2a_example1.png "")

use color parameters **context menu** to import current foreground or background colors if needed
and run the script

![](./img/b2a_example2.png "")

at the end a new layer named "Background to Alpha" will be created with the same subject of the
processed layer but without the background color.

![](./img/b2a_example3.png "")

