from shared import StandardObject, Signature
from dict import DictInfo
from struct import Struct

def generate_lut_commands(lut: list[float]) -> bytes:
    assert len(lut) == 256
    command = b'\xc8\x01\xff\x07'
    values = [min(int(i * 0x1000), 0xfff) for i in lut]
    diffs = [min(int(abs(j - i) * 0x800), 0x7ff) for i, j in zip(lut, lut[1:])] + [0]
    fixed = [((d << 12) | v).to_bytes(4, 'little') for v, d in zip(values, diffs)]
    assert len(fixed) == 256
    return fixed[0] + command + b''.join(fixed[1:129]) + command + b''.join(fixed[129:])

class LutTable(StandardObject):
    struct = Struct('Iiiii')
    type = 0x80000000
    name = ''
    some_bool = True
    lut: list[float]
    def __init__(self):
        self.lut = [1-abs(i/128) for i in range(-128, 128)]
    def values(self):
        return (self.type, self.name, self.some_bool, generate_lut_commands(self.lut))


class LUTS(StandardObject):
    struct = Struct('I4siiiiii')
    type = 0x04000000
    signature = Signature("LUTS")
    revision = 0x04000000
    name = ''
    user_data: DictInfo
    info: DictInfo
    def __init__(self):
        self.user_data = DictInfo()
        self.tables = DictInfo()
    def values(self):
        return (self.type, self.signature, self.revision, self.name, self.user_data, self.tables)

