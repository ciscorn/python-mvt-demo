import gzip
import time
from collections.abc import Iterable
from pathlib import Path
from typing import cast

import geopandas as gpd
import numpy as np
import shapely
import shapely.geometry

# サンプルデータを読み込んで Web Mercator (EPSG:3857) 空間に変換しておく
with gzip.open(Path(__file__).parent / "sapporo-chuo.geojson.gz", "rb") as zf:
    gdf: gpd.GeoDataFrame = gpd.read_file(zf, engine="pyogrio").to_crs(
        "EPSG:3857"
    )  # type: ignore


def iter_features(bbox: tuple[float, float, float, float], buffer: float = 0):
    xmin, ymin, xmax, ymax = bbox
    buf = (xmax - xmin) * buffer
    buffered_bbox = (xmin - buf, ymin - buf, xmax + buf, ymax + buf)

    t = time.time()
    indices = gdf.geometry.sindex.query(shapely.geometry.box(*buffered_bbox))
    if len(indices) == 0:
        return []
    print(f"Query R-tree: {(time.time() - t) * 1000 : .3f} [ms]")

    t = time.time()
    clipped_features = gdf.iloc[indices]
    clipped_geoms = shapely.clip_by_rect(clipped_features.geometry, *buffered_bbox)
    print(f"Clip by rect: {(time.time() - t) * 1000 : .3f} [ms]")

    scale = np.array([xmax - xmin, -ymax + ymin])
    a = np.array([xmin, ymax])

    t = time.time()
    features = []
    for idx, feat in enumerate(clipped_geoms):
        if isinstance(feat, shapely.MultiPolygon):
            polygons = cast(Iterable[shapely.Polygon], feat.geoms)
        elif isinstance(feat, shapely.Polygon):
            polygons = [feat]
        else:
            continue

        for poly in polygons:
            rings = []
            for ring in shapely.get_rings(poly):
                ring: shapely.LinearRing
                # assert poly.exterior.is_ccw is False
                # assert ring.is_ccw
                xy = np.asarray(ring.coords)
                xy = xy[:-1]
                rings.append((xy - a) / scale)

            feat = clipped_features.iloc[idx]
            features.append((rings, feat))
    print(f"Convert to numpy arrays: {(time.time() - t) * 1000 : .3f} [ms]")

    yield from features
