from PIL.Image import Image
from .txob import PixelBasedImage, TXOB, ImageTexture, TextureFormat

def swizzle(im: Image, format: TextureFormat) -> bytes:
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

    bpp_input = 4

    input = im.tobytes()
    output = b''

    for ty in range(im.height // 8):
        for tx in range(im.width // 8):
            tile = bytearray(8*8*format.bytes_per_pixel())
            for y in range(8):
                for x in range(8):
                    input_pixel_offset = ((ty * 8 + y) * im.width + (tx * 8 + x)) * bpp_input
                    pixel = input[input_pixel_offset:input_pixel_offset+bpp_input][::-1]
                    match format:
                        case TextureFormat.RGB8:
                            pixel = pixel[1:]
                        case TextureFormat.RGBA5551:
                            pixel = ((pixel[0] >> 7) | ((pixel[1] & 0xf8) >> 2) | ((pixel[2] & 0xf8) << 3) | ((pixel[3] & 0xf8) << 8)).to_bytes(2, 'little')
                        case TextureFormat.RGB565:
                            pixel = ((pixel[1] >> 3) | ((pixel[2] & 0xfc) << 3) | ((pixel[3] & 0xf8) << 8)).to_bytes(2, 'little')
                        case TextureFormat.RGBA4:
                            pixel = bytes([(pixel[0] >> 4) | (pixel[1] & 0xf0), (pixel[2] >> 4) | (pixel[3] & 0xf0)])
                        case _:
                            raise RuntimeError(f"Unsupported pixel format {format.name}")
                    output_pixel_offset = swizzle_map[y * 8 + x]*len(pixel)
                    tile[output_pixel_offset:output_pixel_offset+len(pixel)] = pixel
            output += tile
    return output

def to_txob(im: Image, format: TextureFormat = TextureFormat.RGBA4, mipmaps = 1) -> ImageTexture:
    txob = ImageTexture()
    txob.width = txob.pixel_based_image.width = im.width
    txob.height = txob.pixel_based_image.height = im.height
    im = im.convert('RGBA')
    txob.hw_format = format
    txob.pixel_based_image.data = swizzle(im, format)
    txob.mipmap_level_count = 1
    return txob