"""Generate the app icon set from the user's artwork (icon-source.png).

- icon-192 / icon-512 / apple-touch-icon : full-bleed (the art already has a
  background that runs to every edge).
- icon-512-maskable : the art is scaled to ~89% with its background edge-extended
  to the borders, so Android/Chrome's circular mask never clips the cat's ears/chin
  while the colour still bleeds to the edges.
"""
from PIL import Image
import numpy as np

SRC = "icon-source.png"
src = Image.open(SRC).convert("RGB")            # drop alpha; background is opaque
S = src.size[0]

def full(size):
    return src.resize((size, size), Image.LANCZOS)

def maskable(size, pad_frac=0.11):
    arr = np.asarray(src)
    p = int(S * pad_frac / 2)                    # margin added on every side
    padded = np.pad(arr, ((p, p), (p, p), (0, 0)), mode="edge")
    return Image.fromarray(padded).resize((size, size), Image.LANCZOS)

full(512).save("icon-512.png")
full(192).save("icon-192.png")
full(180).save("apple-touch-icon.png")
maskable(512).save("icon-512-maskable.png")
print("icons written from", SRC)
