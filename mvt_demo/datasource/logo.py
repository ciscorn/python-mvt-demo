import random
from pathlib import Path

import numpy as np
from PIL import Image

IMG = Image.open(Path(__file__).parent / "logo01.png")


def get_points(sigma: float = 0):
    width, height = IMG.size
    points = []
    for _i in range(100000):
        x = random.random()
        y = random.random()
        _, _, _, a = IMG.getpixel((int(x * (width - 1)), int(y * (height - 1))))
        if a > 128:
            x += random.normalvariate(0, sigma)
            y += random.normalvariate(0, sigma)
            points.append((x, y))

    return np.array(points)
