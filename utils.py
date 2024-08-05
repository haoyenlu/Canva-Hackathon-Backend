import PIL
import PIL.Image
import io
import base64
from potrace import Bitmap, POTRACE_TURNPOLICY_MINORITY  



def image_to_b64(image: PIL.Image):
    buffer = io.BytesIO()   
    image.save(buffer, format="PNG")
    img_bytes = base64.b64encode(buffer.getvalue()) # encode to bytes
    img_ascii = img_bytes.decode('ascii') # decode to ascii
    return img_ascii
                  


def transparent_to_white(image: PIL.Image):
    width , height = image.size
    pixels = image.load()
    white = (255,255,255,255)
    for x in range(width):
        for y in range(height):
            if pixels[x,y][3] < 100: # conditioned on transparent value
                pixels[x,y] = white


    return image


def image_to_svg(image: PIL.Image, blacklevel = 0.6):
    bm = Bitmap(image, blacklevel=blacklevel)
    plist = bm.trace(
        turdsize=2,
        turnpolicy=POTRACE_TURNPOLICY_MINORITY,
        alphamax=1,
        opticurve=False,
        opttolerance=2,
    )

    svg = ""
    svg += f'''<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{image.width}" height="{image.height}" viewBox="0 0 {image.width} {image.height}">'''
    parts = []
    for curve in plist:
        fs = curve.start_point
        parts.append(f"M{fs.x},{fs.y}")
        for segment in curve.segments:
            if segment.is_corner:
                a = segment.c
                b = segment.end_point
                parts.append(f"L{a.x},{a.y}L{b.x},{b.y}")
            else:
                a = segment.c1
                b = segment.c2
                c = segment.end_point
                parts.append(f"C{a.x},{a.y} {b.x},{b.y} {c.x},{c.y}")
        parts.append("z")
    svg += f'<path stroke="none" fill="black" fill-rule="evenodd" d="{"".join(parts)}"/>'
    svg += "</svg>"

    return svg