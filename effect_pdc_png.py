#!/usr/bin/env python3
"""
Embed an image of a resulting pdc in the document.
"""

from pdc_converter import PDCConverter

import inkex
from inkex import Image

import urllib.request as urllib
import urllib.parse as urlparse
from base64 import encodebytes

class PdcPngEffectInkscape(inkex.EffectExtension):
    """"""

    def add_arguments(self, pars):
        pars.add_argument("--tab")
        pars.add_argument("--platform", type=inkex.Boolean, dest="platform")
        pars.add_argument("--no-antialiasing", type=inkex.Boolean, dest="no_antialiasing")
        pars.add_argument("--sunlight-colors", type=inkex.Boolean, dest="sunlight_colors")
        pars.add_argument("--background-color", dest="background_color")
        pars.add_argument("--offset", type=int, dest="offset")

    def effect(self):
        pdc = PDCConverter(self.svg, self.options)
        pdc.crop([0, 0,
                  self.svg.viewport_width + (2 * self.options.offset),
                  self.svg.viewport_height + (2 * self.options.offset)])

        self.embed_image(self.svg, pdc.to_png())

    def embed_image(self, svg, image):
        tag = Image(href=f"data:image/png;base64,{encodebytes(image).decode("ascii")}",
                    style="image-rendering:optimizeSpeed",
                    x=str(self.options.offset * -1),
                    y=str((self.svg.viewport_height + (3 * self.options.offset)) * -1))

        self.svg.insert(0, tag)

if __name__ == "__main__":
    PdcPngEffectInkscape().run()

