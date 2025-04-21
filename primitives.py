from shared import StandardObject, List
from struct import Struct

class IndexStream(StandardObject):
    struct = Struct('ib?xxiiiiiiiii')
    data_type = 0x1401
    primitive_mode = 0
    is_invisible = False
    face_data: b''
    buffer_object = 0
    location_flag = 0
    command_cache = 0
    command_cache_size = 0
    location_address = 0
    memory_area = 0
    bounding_box_offset = 0
    def values(self) -> tuple:
        return (self.data_type, self.primitive_mode, self.is_invisible, self.face_data,
        self.buffer_object, self.location_flag, self.command_cache, self.command_cache_size,
        self.location_address, self.memory_area, self.bounding_box_offset)


class Primitive(StandardObject):
    struct = Struct('iiiiii')
    index_streams: List[IndexStream]
    buffer_objects: List[int]
    flags = 0
    command_allocator = 0
    def __init__(self):
        self.index_streams = List()
        self.buffer_objects = List()
    def values(self) -> tuple:
        return (self.index_streams, self.buffer_objects, self.flags, self.command_allocator)

class PrimitiveSet(StandardObject):
    struct = Struct('iiiii')
    related_bones: List[int]
    skinning_mode = 0
    primitives: List[Primitive]
    def __init__(self):
        self.related_bones = List()
        self.primitives = List()
    def values(self) -> tuple:
        return (self.related_bones, self.skinning_mode, self.primitives)

class VertexAttribute(StandardObject):
    type: int
    usage = 0
    flags = 0

class InterleavedVertexStream(VertexAttribute):
    struct = Struct('iiiiiiiiiiii')
    type = 0x40000002
    buffer_object = 0
    location_flag = 0
    vertex_stream_data = b''
    location_address = 0
    memory_area = 0
    vertex_data_entry_size = 0
    vertex_streams: List[VertexAttribute]
    def __init__(self):
        self.vertex_streams = List()
    def values(self):
        return (self.type, self.usage, self.flags, self.buffer_object,
            self.location_flag, self.vertex_stream_data, self.location_address,
            self.memory_area, self.vertex_data_entry_size, self.vertex_streams)

class VertexStream(VertexAttribute):
    struct = Struct('iiiiiiiiiiifi')
    type = 0x40000001
    buffer_object = 0
    location_flag = 0
    vertex_stream_data = b''
    location_address = 0
    memory_area = 0
    format_type = 0
    components_count = 0
    scale = 1
    vert_offset = 0
    def values(self):
        return (self.type, self.usage, self.flags, self.buffer_object, self.location_flag,
            self.vertex_stream_data, self.location_address, self.memory_area,
            self.format_type, self.components_count, self.scale, self.vert_offset)

class VertexParamAttribute(VertexAttribute):
    struct = Struct('iiiiifii')
    type = 0x80000000
    format_type = 0
    components_count = 0
    scale = 0
    attributes: List[float]
    def values(self):
        return (self.type, self.usage, self.flags, self.format_type, self.components_count,
            self.scale, self.attributes)