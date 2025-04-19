from dict import DICT, DictInfo
from shared import InlineObject, Signature
from struct import Struct


class CGFXHeader(InlineObject):
    struct = Struct('4sHhiii')
    offset = 0
    signature = Signature('CGFX')
    endianness = 0xfeff
    header_size = 0x14
    version = 0x5000000
    file_size = 0
    nr_blocks = 1

    def values(self):
        return (self.signature, self.endianness, self.header_size, self.version, self.file_size, self.nr_blocks)

class CGFXData(InlineObject):
    struct = Struct('4si' + DictInfo.struct.format * 15)
    offset = CGFXHeader.offset + CGFXHeader.struct.size
    signature = Signature('DATA')
    section_size = 0
    def __init__(self) -> None:
        super().__init__()
        self.models = DictInfo()
        self.textures = DictInfo()
        self.lookup_tables = DictInfo()
        self.materials = DictInfo()
        self.shaders = DictInfo()
        self.cameras = DictInfo()
        self.lights = DictInfo()
        self.fogs = DictInfo()
        self.scenes = DictInfo()
        self.skeletal_animations = DictInfo()
        self.material_animations = DictInfo()
        self.visibility_animations = DictInfo()
        self.camera_animations = DictInfo()
        self.light_animations = DictInfo()
        self.emitters = DictInfo()
    def values(self) -> tuple:
        return (self.signature, self.section_size, self.models, self.textures, self.lookup_tables,
                self.materials, self.shaders, self.cameras, self.lights, self.fogs, self.scenes,
                self.skeletal_animations, self.material_animations, self.visibility_animations,
                self.camera_animations, self.light_animations, self.emitters)

class CGFX(InlineObject):
    struct = Struct(CGFXHeader.struct.format + CGFXData.struct.format)
    offset = 0
    header: CGFXHeader
    data: CGFXData

    def __init__(self) -> None:
        super().__init__()
        self.header = CGFXHeader()
        self.data = CGFXData()

    def values(self) -> tuple:
        return (self.header, self.data)