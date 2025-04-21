from shared import StandardObject, Signature, Reference
from dict import DictInfo
from struct import Struct
from abc import abstractmethod, ABC

class TXOB(StandardObject, ABC):
    struct = Struct('i4siiii')
    type: int
    signature = Signature('TXOB')
    revision = 0x5000000
    name = ''
    user_data: DictInfo
    def __init__(self):
        self.user_data = DictInfo()
    def values(self):
        return (self.type, self.signature, self.revision,
            self.name, self.user_data)
    @abstractmethod
    def width(self) -> int:
        pass
    @abstractmethod
    def height(self) -> int:
        pass

class ReferenceTexture(TXOB):
    struct = Struct(TXOB.struct.format + 'ii')
    type = 0x20000004
    txob: TXOB
    def __init__(self, txob: TXOB):
        super().__init__()
        self.txob = txob
    def values(self):
        return (*super().values(), self.txob.name, Reference(self.txob))
    def width(self):
        return self.txob.width()
    def height(self):
        return self.txob.height()

class PixelBasedTexture(TXOB):
    # padding is written to at runtime
    struct = Struct(TXOB.struct.format + 'iiiiixxxxii')
    height = 0
    width = 0
    gl_format = 0
    gl_type = 0
    mipmap_level_count = 0
    location_flag = 0
    hw_format = 0
    def values(self):
        return (*super().values(), self.height, self.width, self.gl_format, self.gl_type,
            self.mipmap_level_count, self.location_flag, self.hw_format)
    def width(self):
        return self.width
    def height(self):
        return self.height

class PixelBasedImage(StandardObject):
    struct = Struct('iiiiiiii')
    height = 0
    width = 0
    data = b''
    dynamic_allocator = 0
    bits_per_pixel = 0
    location_address = 0
    memory_address = 0
    def values(self):
        return (self.height, self.width, self.data,
            self.dynamic_allocator, self.bits_per_pixel, self.location_address,
            self.memory_address)

class ImageTexture(PixelBasedTexture):
    struct = Struct(PixelBasedTexture.struct.format + 'i')
    type = 0x20000011
    pixel_based_image: PixelBasedImage
    def __init__(self):
        super().__init__()
        self.pixel_based_image = PixelBasedImage()
    def values(self):
        return (*super().values(), self.pixel_based_image)