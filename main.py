from cgfx import CGFX
from cmdl import CMDL
from shared import StringTable


def write(cgfx: CGFX) -> bytes:
    strings = StringTable()
    imag = StringTable()
    offset = cgfx.prepare(0, strings, imag)
    offset = strings.prepare(offset)
    if not imag.empty():
        cgfx.header.nr_blocks = 2
        offset += 8 # IMAG header
    offset = imag.prepare(offset)
    cgfx.header.file_size = offset
    cgfx.data.section_size = offset - cgfx.data.offset
    data = cgfx.write(strings, imag)
    data += strings.write()
    if not imag.empty():
        data += b'IMAG' + imag.size().to_bytes(4, 'little') + imag.write()
    return data

if __name__ == '__main__':
    cgfx = CGFX()
    cgfx.data.models.dict.add("main", CMDL())
    with open("test.cgfx", "wb") as f:
        f.write(write(cgfx))