from PIL.Image import Image
from txob import PixelBasedImage, TXOB, ImageTexture

def swizzle(im: Image) -> bytes:
    swizzle_map = [
        0x00, 0x01, 0x04, 0x05, 0x10, 0x11, 0x14, 0x15,
        0x02, 0x03, 0x06, 0x07, 0x12, 0x13, 0x16, 0x17,
        0x08, 0x09, 0x0c, 0x0d, 0x18, 0x19, 0x1c, 0x1d,
        0x0a, 0x0b, 0x0e, 0x0f, 0x1a, 0x1b, 0x1e, 0x1f,
        0x20, 0x21, 0x24, 0x25, 0x30, 0x31, 0x34, 0x35,
        0x22, 0x23, 0x26, 0x27, 0x32, 0x33, 0x36, 0x37,
        0x28, 0x29, 0x2c, 0x2d, 0x38, 0x39, 0x3c, 0x3d,
        0x2a, 0x2b, 0x2e, 0x2f, 0x3a, 0x3b, 0x3e, 0x3f,
    ]

    bytes_per_pixel = 4

    input = im.tobytes()
    output = b''

    for ty in range(im.height // 8):
        for tx in range(im.width // 8):
            tile = bytearray(8*8*bytes_per_pixel)
            for y in range(8):
                for x in range(8):
                    input_pixel_offset = ((ty * 8 + y) * im.width + (tx * 8 + x)) * bytes_per_pixel
                    pixel = input[input_pixel_offset:input_pixel_offset+bytes_per_pixel][::-1]
                    output_pixel_offset = swizzle_map[y * 8 + x]*bytes_per_pixel
                    tile[output_pixel_offset:output_pixel_offset+bytes_per_pixel] = pixel
            output += tile
    return output

def to_txob(im: Image) -> PixelBasedImage:
    txob = ImageTexture()
    txob.width = txob.pixel_based_image.width = im.width
    txob.height = txob.pixel_based_image.height = im.height
    # TODO be smarter
    im = im.convert('RGBA')
    txob.gl_format = 0x6752
    txob.gl_type = 0x8033
    txob.hw_format = 0
    txob.pixel_based_image.bits_per_pixel = 8 * len(im.mode)
    txob.pixel_based_image.data = swizzle(im)
    txob.mipmap_level_count = 1
    return txob