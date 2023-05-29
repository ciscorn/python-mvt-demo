import time

import numpy as np

from mvt_demo.mvt import vector_tile_pb2 as pb
from mvt_demo.projection import xyz_to_webmercator_bbox

from .datasource import font, sapporo

# MVTのジオメトリで使われるコマンドID
GEOM_COMMAND_MOVE_TO = 1
GEOM_COMMAND_LINE_TO = 2
GEOM_COMMAND_CLOSE_PATH = 7

GEOM_COMMAND_MOVE_TO_WITH_COUNT1 = 1 << 3 | GEOM_COMMAND_MOVE_TO
GEOM_COMMAND_CLOSE_PATH_WITH_COUNT1 = 1 << 3 | GEOM_COMMAND_CLOSE_PATH


class TagsEncoder:
    __slot__ = ("keys", "values", "_key_to_index", "_value_to_index")

    def __init__(self):
        self.keys: list[str] = []
        self.values: list[pb.Tile.Value] = []
        self._key_to_index = {}
        self._value_to_index = {}

    def encode_key(self, key: str) -> int:
        if (idx := self._key_to_index.get(key)) is not None:
            return idx
        else:
            idx = len(self.keys)
            self._key_to_index[key] = idx
            self.keys.append(key)
            return idx

    def encode_value(self, value: str | int | float | bool) -> int:
        if (idx := self._value_to_index.get(value)) is not None:
            return idx
        else:
            idx = len(self.values)
            self._value_to_index[value] = idx
            if isinstance(value, str):
                v = pb.Tile.Value(string_value=value)
            elif isinstance(value, int):
                v = pb.Tile.Value(int_value=value)
                self.values.append(pb.Tile.Value(int_value=value))
            elif isinstance(value, float):
                v = pb.Tile.Value(float_value=value)
            elif isinstance(value, bool):
                v = pb.Tile.Value(bool_value=value)
            else:
                raise TypeError(f"Unsupported type: {type(value)}")
            self.values.append(v)
            return idx


class GeometryEncoder:
    def __init__(self, extent: int = 4096):
        self.extent: int = extent
        self.prev_x: int = 0
        self.prev_y: int = 0
        self.geom: list[int] = []

    def reset(self):
        self.prev_x = 0
        self.prev_y = 0
        self.geom = []

    def draw_points(self, points):
        prev_x = self.prev_x
        prev_y = self.prev_y
        geom = self.geom
        points *= self.extent
        points += 0.5
        points = points.astype(int)
        geom.append(len(points) << 3 | GEOM_COMMAND_MOVE_TO)  # 下位3ビットがコマンドID、他29ビットが頂点数
        for x, y in points:
            dx = x - prev_x
            dy = y - prev_y
            geom.append((dx << 1) ^ (dx >> 31))  # zigzag encoding
            geom.append((dy << 1) ^ (dy >> 31))  # zigzag encoding
            prev_x = x
            prev_y = y
        self.prev_x = prev_x
        self.prev_y = prev_y

    def draw_linestring(self, points):
        self._draw_path(points, close_path=False)

    def draw_polygon_ring(self, points):
        self._draw_path(points, close_path=True)

    def _draw_path(self, points, close_path: bool = False):
        prev_x = self.prev_x
        prev_y = self.prev_y
        points *= self.extent
        points += 0.5
        points = points.astype(int)
        # moveTo
        x, y = points[0]
        first_dx = x - prev_x
        first_dy = y - prev_y
        prev_x = x
        prev_y = y
        # lineTo x (N-1)
        linetos = []
        for x, y in points[1:]:
            dx = x - prev_x
            dy = y - prev_y
            if dx != 0 or dy != 0:
                linetos.append((dx << 1) ^ (dx >> 31))  # zigzag encoding
                linetos.append((dy << 1) ^ (dy >> 31))  # zigzag encoding
                prev_x = x
                prev_y = y

        if linetos:
            geom = self.geom
            geom.append(GEOM_COMMAND_MOVE_TO_WITH_COUNT1)  # 下位3ビットがコマンドID、他29ビットが頂点数
            geom.append((first_dx << 1) ^ (first_dx >> 31))  # zigzag encoding
            geom.append((first_dy << 1) ^ (first_dy >> 31))  # zigzag encoding
            geom.append((len(linetos) // 2) << 3 | GEOM_COMMAND_LINE_TO)
            geom.extend(linetos)
            if close_path:
                geom.append(GEOM_COMMAND_CLOSE_PATH_WITH_COUNT1)
            self.prev_x = prev_x
            self.prev_y = prev_y


def generate_mvt_tile(
    *, z: int, x: int, y: int, extent: int = 4096, buffer: int = 64
) -> bytes | None:
    """
    指定されたXYZのベクタータイル (MVT) を生成する
    """

    geom_encoder = GeometryEncoder(extent=extent)
    tags_encoder = TagsEncoder()
    bbox = xyz_to_webmercator_bbox(x=x, y=y, z=z)
    log_texts = []

    t = time.time()
    features = []
    for rings, props in sapporo.iter_features(bbox, buffer=buffer / extent):
        # ジオメトリをエンコードする
        geom_encoder.reset()
        for ring in rings:
            geom_encoder.draw_polygon_ring(ring)

        # ジオメトリが空の場合はスキップする
        if not geom_encoder.geom:
            continue

        # 属性値をエンコードする
        tags = []
        for k, v in props.items():
            if k != "geometry" and v is not None:
                tags.append(tags_encoder.encode_key(k))
                tags.append(tags_encoder.encode_value(v))
        features.append(
            pb.Tile.Feature(
                id=int(props.name),
                tags=tags,
                type=pb.Tile.POLYGON,
                geometry=geom_encoder.geom,
            )
        )
    log_texts.append(f"{len(features)} features.")
    log_texts.append(f"Render geoms: {(time.time() - t) * 1000 : .0f} [ms]")

    if not features:
        return None

    polygon_layer = pb.Tile.Layer(
        version=2,
        name="polygons",
        keys=tags_encoder.keys,
        values=tags_encoder.values,
        features=features,
        extent=extent,
    )

    features = []
    for i, text in enumerate(log_texts):
        geom_encoder.reset()
        for stroke in font.get_strokes(text):
            stroke += np.array([0.01, 0.03 + 0.04 * i])
            geom_encoder.draw_linestring(stroke)
        features.append(
            pb.Tile.Feature(
                tags=[],
                type=pb.Tile.LINESTRING,
                geometry=geom_encoder.geom,
            )
        )
    text_layer = pb.Tile.Layer(
        version=2,
        name="texts",
        keys=[],
        values=[],
        features=features,
        extent=extent,
    )

    tile = pb.Tile(layers=[polygon_layer, text_layer])

    t = time.time()
    serialized = tile.SerializeToString()
    print(f"Serialize to MVT: {(time.time() - t) * 1000 : .3f} [ms]")

    return serialized
