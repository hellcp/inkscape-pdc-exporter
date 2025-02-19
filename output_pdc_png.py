#!/usr/bin/env python3
"""
Run the pdc module on the svg output.
"""
import subprocess
import tempfile

import inkex

class PdcPngInkscape(inkex.OutputExtension):
    """Pdc Png Inkscape Extension"""

    def add_arguments(self, pars):
        pars.add_argument("--tab")
        pars.add_argument("--platform", type=inkex.Boolean, dest="platform")
        pars.add_argument("--no-antialiasing", type=inkex.Boolean, dest="no_antialiasing")
        pars.add_argument("--background-color", dest="background_color")
        pars.add_argument("--offset", type=int, dest="offset")

    def save(self, stream):
        infile = tempfile.NamedTemporaryFile(delete_on_close=False)
        infile.write(self.svg.tostring())
        infile.close()
        outfile = tempfile.NamedTemporaryFile()
        platform = "basalt" if self.options.platform else "aplite"
        command = ["./pdc_tool", infile.name, "png", outfile.name,
                   f"--platform={platform}",
                   f"--background-color={self.options.background_color}",
                   f"--offset={self.options.offset},{self.options.offset}"]
        if self.options.no_antialiasing:
            command.append('--no-antialiasing')
        subprocess.run(command)
        stream.write(outfile.read())
        outfile.close()

if __name__ == "__main__":
    PdcPngInkscape().run()
