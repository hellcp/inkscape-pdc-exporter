#!/usr/bin/env python3
"""
Run the pdc module on the svg output.
"""
from pdc_converter import PDCConverter

import inkex

class PdcPngInkscape(inkex.OutputExtension):
    """Pdc Png Inkscape Extension"""

    def add_arguments(self, pars):
        pars.add_argument("--tab")
        pars.add_argument("--platform", type=inkex.Boolean, dest="platform")
        pars.add_argument("--no-antialiasing", type=inkex.Boolean, dest="no_antialiasing")
        pars.add_argument("--background-color", dest="background_color")
        pars.add_argument("--offset", type=int, dest="offset")
        pars.add_argument("--crop", type=inkex.Boolean, dest="crop")

    def save(self, stream):
        pdc = PDCConverter(self.svg, self.options)

        if self.options.crop:
            pdc.crop([0, 0,
                      self.svg.viewport_width + (2 * self.options.offset),
                      self.svg.viewport_height + (2 * self.options.offset)])

        stream.write(pdc.to_png())

if __name__ == "__main__":
    PdcPngInkscape().run()
