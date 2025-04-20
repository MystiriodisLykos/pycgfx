from shared import InlineObject, StandardObject, Signature, Matrix, Vector3, Reference
from dict import DictInfo
from struct import Struct
from txob import TXOB

class Color(InlineObject):
    def __init__(self, r, g, b, a):
        self.r = r
        self.g = g
        self.b = b
        self.a = a
    def values(self):
        return (r, g, b, a)

class ColorByte(Color):
    struct = Struct('bbbb')

class ColorFloat(Color):
    struct = Struct('ffff')
    def as_byte(self) -> ColorByte:
        return ColorByte(self.r * 255, self.g * 255, self.b * 255, self.a * 255)

class PicaCommand(InlineObject):
    struct = Struct('ii')
    def __init__(self, param, head):
        self.param = param
        self.head = head
    def values(self):
        return (self.param, self.head)

class MaterialColor(InlineObject):
    struct = Struct('ffff' * (3 + 2 + 6) + 'bbbb' * (3 + 2 + 6) + 'i')
    emission = ColorFloat(0, 0, 0, 0)
    ambient = ColorFloat(1, 1, 1, 1)
    diffuse = ColorFloat(1, 1, 1, 1)
    specular: list[ColorFloat]
    constant: list[ColorFloat]
    command_cache = 0
    def __init__(self):
        self.specular = [ColorFloat(0.33, 0.33, 0.33, 0), ColorFloat(0, 0, 0, 0)]
        self.constant = [ColorFloat(0, 0, 0, 0) for _ in range(6)]
    def values(self):
        return (self.emission, self.ambient, self.diffuse, *self.specular, *self.constant,
            self.emission.as_byte(), self.ambient.as_byte(), self.diffuse.as_byte(),
            *(x.as_byte() for x in self.specular + self.constant),
            self.command_cache)

class Rasterization(InlineObject):
    struct = Struct('iifii')
    flags = 0
    culling_mode = 3
    polygon_offset_unit = 0
    command = PicaCommand(0, 0x00010040)
    def values(self):
        return (self.flags, self.culling_mode, self.polygon_offset_unit, self.command)

class DepthOperation(InlineObject):
    struct = Struct('iiiiii')
    flags = 3
    commands: list[PicaCommand]
    def __init__(self):
        self.commands = [PicaCommand(0x41, 0x10107), PicaCommand(0x3000000, 0x80126)]
    def values(self):
        return (self.flags, *self.commands)

class BlendOperation(InlineObject):
    struct = Struct('iffffiiiiii')
    mode = 0
    blend = ColorFloat(0, 0, 0, 1)
    commands: list[PicaCommand]
    def __init__(self):
        self.commands = [PicaCommand(0x40100, 0x803f0100), PicaCommand(0x76760000, 0), PicaCommand(0xff000000, 0)]
    def values(self):
        return (self.mode, self.blend, *self.commands)

class FragmentOperation(InlineObject):
    struct = Struct(DepthOperation.struct.format + BlendOperation.struct.format + 'iiii')
    depth_operation: DepthOperation
    blend_operation: BlendOperation
    stencil_commands: list[PicaCommand]
    def __init__(self):
        self.depth_operation = DepthOperation()
        self.blend_operation = BlendOperation()
        self.stencil_commands = [PicaCommand(0xff000000, 0xd0105), PicaCommand(0, 0xf0106)]
    def values(self):
        return (self.depth_operation, self.blend_operation, self.stencil_commands)

class TextureCoordinator(InlineObject):
    struct = Struct('iiiifffffi' + 'f' * 12)
    source_coordinate = 0
    projection = 0
    reference_camera = 0
    matrix_mode = 0
    scale_u = 0
    scale_v = 0
    rotate = 0
    translate_u = 0
    translate_v = 0
    enabled = 0
    transform_matrix: Matrix
    def __init__(self):
        self.transform_matrix = Matrix(Vector3(1, 0, 0), Vector3(0, 0, 1), Vector3(0, 0, 0), Vector3(0, 1, 0))
    def values(self):
        return (self.source_coordinate, self.projection, self.reference_camera,
            self.matrix_mode, self.scale_u, self.scale_v, self.rotate,
            self.translate_u, self.translate_v, self.transform_matrix)

class TextureSampler(StandardObject):
    struct = Struct('iii')
    type = 0
    owner: TexInfo
    min_filter = 0
    def __init__(self, owner):
        self.owner = owner
    def values(self):
        return (self.type, Reference(self.owner), self.min_filter)

class TexInfo(StandardObject):
    struct = Struct('iiiiiiiihh' + 'x' * (9*4) + 'i')
    type = 0x80000000
    dynamic_allocator = 0
    txob: TXOB
    sampler: TextureSampler
    commands: list[PicaCommand]
    command_size_to_send = 0x38
    def __init__(self, txob: TXOB):
        self.txob = txob
        self.sampler = TextureSampler(self)
        self.commands = [PicaCommand(0, 0x1008e), PicaCommand(0xFF000000, 0x809f0081),
            PicaCommand((txob.width() << 16) | txob.height(), 0x1002206), PicaCommand(0, 0),
            PicaCommand(0, 0), PicaCommand(0, 0), PicaCommand(0, 0)]
    def values(self):
        return (self.type, self.dynamic_allocator, self.txob, self.sampler_offset,
            *self.commands, self.command_size_to_send)

class MTOB(StandardObject):
    type = 0x8000000
    signature = Signature("MTOB")
    revision = 0x6000003
    name = ''
    user_data: DictInfo
    flags = 0
    texture_coordinates_config = 0
    transluscency_kind = 0
    material_color: MaterialColor
    rasterization: Rasterization
    fragment_operations: FragmentOperation
    used_texture_coordinates_count = 0
    texture_coordinators: list[TextureCoordinator]
    texture_mappers: list[TexInfo | None]
    shdr = None
    fragment_shader = None
    shader_program_description_index = 0
    shader_parameters_count = 0
    shader_parameters_pointer_table = 0
    light_set_index = 0
    fog_index = 0
    material_id = 0
    def __init__(self):
        self.user_data = DictInfo()
        self.material_color = MaterialColor()
        self.rasterization = Rasterization()
        self.fragment_operations = FragmentOperation()
        self.texture_coordinators = [TextureCoordinator() for _ in range(3)]
        self.texture_mappers = [None, None, None, None]
    def values(self):
        return (self.type, self.signature, self.revision, self.name, self.user_data,
            self.flags, self.texture_coordinates_config, self.transluscency_kind,
            self.material_color, self.rasterization, self.fragment_operations,
            self.used_texture_coordinates_count, *self.texture_coordinators,
            *self.texture_mappers, self.fragment_shader, self.shader_program_description_index,
            self.shader_parameters_count, self.shader_parameters_pointer_table,
            self.light_set_index, self.fog_index,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, # TODO hashes
            self.material_id)



    