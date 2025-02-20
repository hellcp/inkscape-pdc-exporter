#!/usr/bin/env python3
"""
Run the pdc module on the svg output.
"""
import subprocess
import tempfile
import sys

import inkex

class PdcInkscape(inkex.OutputExtension):
    """PDC Inkscape Extension"""

    def save(self, stream):
        with tempfile.NamedTemporaryFile(delete=False) as infile:
            infile.write(self.svg.tostring())
            infile_path = infile.name

        with tempfile.NamedTemporaryFile() as outfile:
            command = [
                "./pdc_tool", infile_path, "pdc", outfile.name
            ]
            messages = subprocess.run(command, check=True, capture_output=True)
            sys.stderr.write(messages.stderr.decode(sys.stderr.encoding))
            pdc = outfile.read()

        stream.write(pdc)

if __name__ == "__main__":
    PdcInkscape().run()
