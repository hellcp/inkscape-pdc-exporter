import tempfile
import subprocess
import io
from PIL import Image

class PDCConverter:
    def __init__(self, svg, options):
        self.svg = svg
        self.options = options
        self.png = None

    def convert_to_png(self):
        """Converts PDC to PNG using the pdc_tool."""
        with tempfile.NamedTemporaryFile(delete=False) as infile:
            infile.write(self.svg.tostring())
            infile_path = infile.name

        with tempfile.NamedTemporaryFile() as outfile:
            outfile_path = outfile.name
            platform = "basalt" if self.options.platform else "aplite"

            command = [
                "./pdc_tool", infile_path, "png", outfile_path,
                f"--platform={platform}",
                f"--background-color={self.options.background_color}",
                f"--offset={self.options.offset},{self.options.offset}"
            ]
            if self.options.no_antialiasing:
                command.append("--no-antialiasing")

            subprocess.run(command, check=True)
            self.png = outfile.read()

        return self

    def crop(self, crop_box):
        """Crops the image based on the provided crop_box."""
        
        if not self.png:
            self.convert_to_png()

        image = Image.open(io.BytesIO(self.png))
        image = image.crop(crop_box)
        png = io.BytesIO()
        image.save(png, 'PNG')
        self.png = png.getvalue()

        return self

    def to_png(self):
        if not self.png:
            self.convert_to_png()

        return self.png
