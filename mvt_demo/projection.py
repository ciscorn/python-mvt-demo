from math import pi

HALF_CIRCUMFERENCE = pi * 6378137


def xyz_to_webmercator_bbox(
    x: int, y: int, z: int
) -> tuple[float, float, float, float]:
    """Convert XYZ tile coordinates to Web Mercator bbox (xmin, ymin, xmax, ymax)."""

    side = 2 * HALF_CIRCUMFERENCE / (1 << z)
    xmin = side * x - HALF_CIRCUMFERENCE
    ymax = -side * y + HALF_CIRCUMFERENCE
    return (xmin, ymax - side, xmin + side, ymax)
