from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf.internal import python_message as _python_message
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Tile(_message.Message):
    __slots__ = ["layers"]
    class GeomType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class Feature(_message.Message):
        __slots__ = ["attributes", "elevations", "geometric_attributes", "geometry", "id", "spline_degree", "spline_knots", "string_id", "tags", "type"]
        ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
        ELEVATIONS_FIELD_NUMBER: _ClassVar[int]
        GEOMETRIC_ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
        GEOMETRY_FIELD_NUMBER: _ClassVar[int]
        ID_FIELD_NUMBER: _ClassVar[int]
        SPLINE_DEGREE_FIELD_NUMBER: _ClassVar[int]
        SPLINE_KNOTS_FIELD_NUMBER: _ClassVar[int]
        STRING_ID_FIELD_NUMBER: _ClassVar[int]
        TAGS_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        attributes: _containers.RepeatedScalarFieldContainer[int]
        elevations: _containers.RepeatedScalarFieldContainer[int]
        geometric_attributes: _containers.RepeatedScalarFieldContainer[int]
        geometry: _containers.RepeatedScalarFieldContainer[int]
        id: int
        spline_degree: int
        spline_knots: _containers.RepeatedScalarFieldContainer[int]
        string_id: str
        tags: _containers.RepeatedScalarFieldContainer[int]
        type: Tile.GeomType
        def __init__(self, id: _Optional[int] = ..., tags: _Optional[_Iterable[int]] = ..., type: _Optional[_Union[Tile.GeomType, str]] = ..., geometry: _Optional[_Iterable[int]] = ..., attributes: _Optional[_Iterable[int]] = ..., geometric_attributes: _Optional[_Iterable[int]] = ..., elevations: _Optional[_Iterable[int]] = ..., spline_knots: _Optional[_Iterable[int]] = ..., spline_degree: _Optional[int] = ..., string_id: _Optional[str] = ...) -> None: ...
    class Layer(_message.Message):
        __slots__ = ["attribute_scalings", "double_values", "elevation_scaling", "extent", "features", "float_values", "int_values", "keys", "name", "string_values", "tile_x", "tile_y", "tile_zoom", "values", "version"]
        ATTRIBUTE_SCALINGS_FIELD_NUMBER: _ClassVar[int]
        DOUBLE_VALUES_FIELD_NUMBER: _ClassVar[int]
        ELEVATION_SCALING_FIELD_NUMBER: _ClassVar[int]
        EXTENT_FIELD_NUMBER: _ClassVar[int]
        Extensions: _python_message._ExtensionDict
        FEATURES_FIELD_NUMBER: _ClassVar[int]
        FLOAT_VALUES_FIELD_NUMBER: _ClassVar[int]
        INT_VALUES_FIELD_NUMBER: _ClassVar[int]
        KEYS_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        STRING_VALUES_FIELD_NUMBER: _ClassVar[int]
        TILE_X_FIELD_NUMBER: _ClassVar[int]
        TILE_Y_FIELD_NUMBER: _ClassVar[int]
        TILE_ZOOM_FIELD_NUMBER: _ClassVar[int]
        VALUES_FIELD_NUMBER: _ClassVar[int]
        VERSION_FIELD_NUMBER: _ClassVar[int]
        attribute_scalings: _containers.RepeatedCompositeFieldContainer[Tile.Scaling]
        double_values: _containers.RepeatedScalarFieldContainer[float]
        elevation_scaling: Tile.Scaling
        extent: int
        features: _containers.RepeatedCompositeFieldContainer[Tile.Feature]
        float_values: _containers.RepeatedScalarFieldContainer[float]
        int_values: _containers.RepeatedScalarFieldContainer[int]
        keys: _containers.RepeatedScalarFieldContainer[str]
        name: str
        string_values: _containers.RepeatedScalarFieldContainer[str]
        tile_x: int
        tile_y: int
        tile_zoom: int
        values: _containers.RepeatedCompositeFieldContainer[Tile.Value]
        version: int
        def __init__(self, version: _Optional[int] = ..., name: _Optional[str] = ..., features: _Optional[_Iterable[_Union[Tile.Feature, _Mapping]]] = ..., keys: _Optional[_Iterable[str]] = ..., values: _Optional[_Iterable[_Union[Tile.Value, _Mapping]]] = ..., extent: _Optional[int] = ..., string_values: _Optional[_Iterable[str]] = ..., float_values: _Optional[_Iterable[float]] = ..., double_values: _Optional[_Iterable[float]] = ..., int_values: _Optional[_Iterable[int]] = ..., elevation_scaling: _Optional[_Union[Tile.Scaling, _Mapping]] = ..., attribute_scalings: _Optional[_Iterable[_Union[Tile.Scaling, _Mapping]]] = ..., tile_x: _Optional[int] = ..., tile_y: _Optional[int] = ..., tile_zoom: _Optional[int] = ...) -> None: ...
    class Scaling(_message.Message):
        __slots__ = ["base", "multiplier", "offset"]
        BASE_FIELD_NUMBER: _ClassVar[int]
        MULTIPLIER_FIELD_NUMBER: _ClassVar[int]
        OFFSET_FIELD_NUMBER: _ClassVar[int]
        base: float
        multiplier: float
        offset: int
        def __init__(self, offset: _Optional[int] = ..., multiplier: _Optional[float] = ..., base: _Optional[float] = ...) -> None: ...
    class Value(_message.Message):
        __slots__ = ["bool_value", "double_value", "float_value", "int_value", "sint_value", "string_value", "uint_value"]
        BOOL_VALUE_FIELD_NUMBER: _ClassVar[int]
        DOUBLE_VALUE_FIELD_NUMBER: _ClassVar[int]
        Extensions: _python_message._ExtensionDict
        FLOAT_VALUE_FIELD_NUMBER: _ClassVar[int]
        INT_VALUE_FIELD_NUMBER: _ClassVar[int]
        SINT_VALUE_FIELD_NUMBER: _ClassVar[int]
        STRING_VALUE_FIELD_NUMBER: _ClassVar[int]
        UINT_VALUE_FIELD_NUMBER: _ClassVar[int]
        bool_value: bool
        double_value: float
        float_value: float
        int_value: int
        sint_value: int
        string_value: str
        uint_value: int
        def __init__(self, string_value: _Optional[str] = ..., float_value: _Optional[float] = ..., double_value: _Optional[float] = ..., int_value: _Optional[int] = ..., uint_value: _Optional[int] = ..., sint_value: _Optional[int] = ..., bool_value: bool = ...) -> None: ...
    Extensions: _python_message._ExtensionDict
    LAYERS_FIELD_NUMBER: _ClassVar[int]
    LINESTRING: Tile.GeomType
    POINT: Tile.GeomType
    POLYGON: Tile.GeomType
    SPLINE: Tile.GeomType
    UNKNOWN: Tile.GeomType
    layers: _containers.RepeatedCompositeFieldContainer[Tile.Layer]
    def __init__(self, layers: _Optional[_Iterable[_Union[Tile.Layer, _Mapping]]] = ...) -> None: ...
