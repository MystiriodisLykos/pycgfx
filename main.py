from cgfx import CGFX
from cmdl import CMDL, CMDLWithSkeleton, GraphicsAnimationGroup, AnimationGroupMember
from shared import StringTable, Vector3
from txob import ImageTexture, PixelBasedImage, ReferenceTexture
from sobj import SOBJMesh, SOBJShape, SOBJSkeleton, Bone
from primitives import Primitive, PrimitiveSet, InterleavedVertexStream, IndexStream, VertexStream
from mtob import MTOB, ColorFloat, TexInfo, PicaCommand, LinkedShader


def make_demo_cgfx() -> CGFX:
    cgfx = CGFX()
    txob = ImageTexture()
    cgfx.data.textures.add("COMMON1", txob)
    txob.name = 'COMMON1'
    txob.height = 128
    txob.width = 256
    txob.gl_format = 0x6752
    txob.gl_type = 0x8033
    txob.mipmap_level_count = 1
    txob.hw_format = 4

    image = PixelBasedImage()
    txob.pixel_based_image = image
    image.height = 128
    image.width = 256
    image.bits_per_pixel = 16

    with open("red-viper-texture-data.bin", "rb") as f:
        image.data = f.read()

    cmdl = CMDLWithSkeleton()
    cgfx.data.models.add("COMMON", cmdl)
    cmdl.name = "COMMON"
    cmdl.flags = 1
    cmdl.branch_visible = True
    cmdl.flags2 = 1

    skeletal_animation = GraphicsAnimationGroup()
    cmdl.animation_group_descriptions.add("SkeletalAnimation", skeletal_animation)
    skeletal_animation.flags = 1
    skeletal_animation.name = 'SkeletalAnimation'
    skeletal_animation.member_type = 1
    skeletal_animation.blend_operations.add(8)
    skeletal_animation.evalution_timing = 1

    banner = AnimationGroupMember()
    skeletal_animation.members.add('banner', banner)
    banner.type = 0x40000000
    banner.path = 'banner'
    banner.member = 'banner'
    banner.subtype = 0
    banner.string = 'banner'
    
    visibility_animation = GraphicsAnimationGroup()
    cmdl.animation_group_descriptions.add("VisibilityAnimation", visibility_animation)
    visibility_animation.name = 'VisibilityAnimation'
    visibility_animation.member_type = 3
    visibility_animation.blend_operations.add(0)

    is_visible = AnimationGroupMember()
    visibility_animation.members.add('IsVisible', is_visible)
    is_visible.type = 0x10000000
    is_visible.path = 'IsVisible'
    is_visible.object_type = 212
    is_visible.member_type = 1
    is_visible.subtype = 6
    is_visible.some_bool = 1

    meshes_zero_is_visible = AnimationGroupMember()
    visibility_animation.members.add('Meshes[0].IsVisible', meshes_zero_is_visible)
    meshes_zero_is_visible.type = 0x1000000
    meshes_zero_is_visible.path = 'Meshes[0].IsVisible'
    meshes_zero_is_visible.member = '0'
    meshes_zero_is_visible.object_type = 36
    meshes_zero_is_visible.member_type = 1
    meshes_zero_is_visible.subtype = 7

    material_animation = GraphicsAnimationGroup()
    cmdl.animation_group_descriptions.add("MaterialAnimation", material_animation)
    material_animation.name = 'MaterialAnimation'
    material_animation.member_type = 2
    material_animation.evalution_timing = 1
    material_animation.blend_operations.add(3)
    material_animation.blend_operations.add(7)
    material_animation.blend_operations.add(5)
    material_animation.blend_operations.add(2)
    
    member = AnimationGroupMember()
    material_animation.members.add('Materials["mt_banner"].MaterialColor.Emission', member)
    member.type = 0x8000000
    member.path = 'Materials["mt_banner"].MaterialColor.Emission'
    member.member = 'mt_banner'
    member.blend_operation_index = 'MaterialColor'
    member.object_type = 16 * 0
    member.member_type = 16
    member.subtype = 1
    member.string = 'mt_banner'
    
    member = AnimationGroupMember()
    material_animation.members.add('Materials["mt_banner"].MaterialColor.Ambient', member)
    member.type = 0x8000000
    member.path = 'Materials["mt_banner"].MaterialColor.Ambient'
    member.member = 'mt_banner'
    member.blend_operation_index = 'MaterialColor'
    member.object_type = 16 * 1
    member.member_type = 16
    member.subtype = 1
    member.some_bool = 1
    member.string = 'mt_banner'
    
    member = AnimationGroupMember()
    material_animation.members.add('Materials["mt_banner"].MaterialColor.Diffuse', member)
    member.type = 0x8000000
    member.path = 'Materials["mt_banner"].MaterialColor.Diffuse'
    member.member = 'mt_banner'
    member.blend_operation_index = 'MaterialColor'
    member.object_type = 16 * 2
    member.member_type = 16
    member.subtype = 1
    member.some_bool = 2
    member.string = 'mt_banner'
    
    member = AnimationGroupMember()
    material_animation.members.add('Materials["mt_banner"].MaterialColor.Specular0', member)
    member.type = 0x8000000
    member.path = 'Materials["mt_banner"].MaterialColor.Specular0'
    member.member = 'mt_banner'
    member.blend_operation_index = 'MaterialColor'
    member.object_type = 16 * 3
    member.member_type = 16
    member.subtype = 1
    member.some_bool = 3
    member.string = 'mt_banner'
    
    member = AnimationGroupMember()
    material_animation.members.add('Materials["mt_banner"].MaterialColor.Specular1', member)
    member.type = 0x8000000
    member.path = 'Materials["mt_banner"].MaterialColor.Specular1'
    member.member = 'mt_banner'
    member.blend_operation_index = 'MaterialColor'
    member.object_type = 16 * 4
    member.member_type = 16
    member.subtype = 1
    member.some_bool = 4
    member.string = 'mt_banner'
    
    member = AnimationGroupMember()
    material_animation.members.add('Materials["mt_banner"].MaterialColor.Constant0', member)
    member.type = 0x8000000
    member.path = 'Materials["mt_banner"].MaterialColor.Constant0'
    member.member = 'mt_banner'
    member.blend_operation_index = 'MaterialColor'
    member.object_type = 16 * 5
    member.member_type = 16
    member.subtype = 1
    member.some_bool = 5
    member.string = 'mt_banner'
    
    member = AnimationGroupMember()
    material_animation.members.add('Materials["mt_banner"].MaterialColor.Constant1', member)
    member.type = 0x8000000
    member.path = 'Materials["mt_banner"].MaterialColor.Constant1'
    member.member = 'mt_banner'
    member.blend_operation_index = 'MaterialColor'
    member.object_type = 16 * 6
    member.member_type = 16
    member.subtype = 1
    member.some_bool = 6
    member.string = 'mt_banner'
    
    member = AnimationGroupMember()
    material_animation.members.add('Materials["mt_banner"].MaterialColor.Constant2', member)
    member.type = 0x8000000
    member.path = 'Materials["mt_banner"].MaterialColor.Constant2'
    member.member = 'mt_banner'
    member.blend_operation_index = 'MaterialColor'
    member.object_type = 16 * 7
    member.member_type = 16
    member.subtype = 1
    member.some_bool = 7
    member.string = 'mt_banner'
    
    member = AnimationGroupMember()
    material_animation.members.add('Materials["mt_banner"].MaterialColor.Constant3', member)
    member.type = 0x8000000
    member.path = 'Materials["mt_banner"].MaterialColor.Constant3'
    member.member = 'mt_banner'
    member.blend_operation_index = 'MaterialColor'
    member.object_type = 16 * 8
    member.member_type = 16
    member.subtype = 1
    member.some_bool = 8
    member.string = 'mt_banner'
    
    member = AnimationGroupMember()
    material_animation.members.add('Materials["mt_banner"].MaterialColor.Constant4', member)
    member.type = 0x8000000
    member.path = 'Materials["mt_banner"].MaterialColor.Constant4'
    member.member = 'mt_banner'
    member.blend_operation_index = 'MaterialColor'
    member.object_type = 16 * 9
    member.member_type = 16
    member.subtype = 1
    member.some_bool = 9
    member.string = 'mt_banner'
    
    member = AnimationGroupMember()
    material_animation.members.add('Materials["mt_banner"].MaterialColor.Constant5', member)
    member.type = 0x8000000
    member.path = 'Materials["mt_banner"].MaterialColor.Constant5'
    member.member = 'mt_banner'
    member.blend_operation_index = 'MaterialColor'
    member.object_type = 16 * 10
    member.member_type = 16
    member.subtype = 1
    member.some_bool = 10
    member.string = 'mt_banner'
    
    member = AnimationGroupMember()
    material_animation.members.add('Materials["mt_banner"].TextureMappers[0].Sampler.BorderColor', member)
    member.type = 0x2000000
    member.path = 'Materials["mt_banner"].TextureMappers[0].Sampler.BorderColor'
    member.member = 'mt_banner'
    member.blend_operation_index = 'TextureMappers[0].Sampler'
    member.object_type = 12
    member.member_type = 16
    member.subtype = 2
    member.some_bool = 0
    member.string = 'mt_banner'
    
    member = AnimationGroupMember()
    material_animation.members.add('Materials["mt_banner"].TextureMappers[0].Texture', member)
    member.type = 0x20000000
    member.path = 'Materials["mt_banner"].TextureMappers[0].Texture'
    member.member = 'mt_banner'
    member.blend_operation_index = 'TextureMappers[0]'
    member.object_type = 8
    member.member_type = 4
    member.res_material_ptr = 1
    member.subtype = 3
    member.some_bool = 0
    member.string = 'mt_banner'
    
    member = AnimationGroupMember()
    material_animation.members.add('Materials["mt_banner"].FragmentOperation.BlendOperation.BlendColor', member)
    member.type = 0x4000000
    member.path = 'Materials["mt_banner"].FragmentOperation.BlendOperation.BlendColor'
    member.member = 'mt_banner'
    member.blend_operation_index = 'FragmentOperation.BlendOperation'
    member.object_type = 4
    member.member_type = 16
    member.subtype = 4
    member.some_bool = 0
    member.string = 'mt_banner'
    
    member = AnimationGroupMember()
    material_animation.members.add('Materials["mt_banner"].TextureCoordinators[0].Scale', member)
    member.type = 0x80000000
    member.path = 'Materials["mt_banner"].FragmentOperation.TextureCoordinators[0].Scale'
    member.member = 'mt_banner'
    member.blend_operation_index = 'TextureCoordinators[0]'
    member.object_type = 16
    member.member_type = 8
    member.res_material_ptr = 2
    member.subtype = 5
    member.some_bool = 0
    member.string = 'mt_banner'
    
    member = AnimationGroupMember()
    material_animation.members.add('Materials["mt_banner"].TextureCoordinators[0].Rotate', member)
    member.type = 0x80000000
    member.path = 'Materials["mt_banner"].FragmentOperation.TextureCoordinators[0].Rotate'
    member.member = 'mt_banner'
    member.blend_operation_index = 'TextureCoordinators[0]'
    member.object_type = 24
    member.member_type = 4
    member.res_material_ptr = 3
    member.subtype = 5
    member.some_bool = 1
    member.string = 'mt_banner'
    
    member = AnimationGroupMember()
    material_animation.members.add('Materials["mt_banner"].TextureCoordinators[0].Translate', member)
    member.type = 0x80000000
    member.path = 'Materials["mt_banner"].FragmentOperation.TextureCoordinators[0].Translate'
    member.member = 'mt_banner'
    member.blend_operation_index = 'TextureCoordinators[0]'
    member.object_type = 28
    member.member_type = 8
    member.res_material_ptr = 2
    member.subtype = 5
    member.some_bool = 2
    member.string = 'mt_banner'

    mesh = SOBJMesh(cmdl)
    cmdl.meshes.add(mesh)
    mesh.mesh_node_visibility_index = 65535

    shape = SOBJShape()
    cmdl.shapes.add(shape)
    shape.oriented_bounding_box.center_pos = Vector3(0, -1, 0)
    shape.oriented_bounding_box.bb_size = Vector3(26, 13, 0)
    
    primitive_set = PrimitiveSet()
    shape.primitive_sets.add(primitive_set)
    primitive_set.related_bones.add(0)
    
    primitive = Primitive()
    primitive_set.primitives.add(primitive)
    
    index_stream = IndexStream()
    primitive.index_streams.add(index_stream)
    index_stream.data_type = 0x1401
    index_stream.primitive_mode = 0
    index_stream.is_invisible = True
    index_stream.face_data = bytes([0, 1, 2, 1, 3, 2])
    primitive.buffer_objects.add(0)
    primitive.flags = 8
    
    interleaved_vertex_stream = InterleavedVertexStream()
    shape.vertex_attributes.add(interleaved_vertex_stream)
    interleaved_vertex_stream.usage = 0x15
    interleaved_vertex_stream.flags = 2
    interleaved_vertex_stream.vertex_data_entry_size = 20
    interleaved_vertex_stream.vertex_stream_data = bytes([
        0x00, 0x00, 0x50, 0xC1, 0x00, 0x00, 0xF0, 0xC0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x50, 0x41, 0x00, 0x00, 0xF0, 0xC0, 0x00, 0x00, 0x00, 0x00, 
        0x00, 0x00, 0x80, 0x3F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x50, 0xC1, 0x00, 0x00, 0xB0, 0x40, 
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x80, 0x3F, 0x00, 0x00, 0x50, 0x41, 
        0x00, 0x00, 0xB0, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x80, 0x3F, 0x00, 0x00, 0x80, 0x3F, 
    ])

    position_stream = VertexStream()
    interleaved_vertex_stream.vertex_streams.add(position_stream)
    position_stream.usage = 0
    position_stream.flags = 0
    position_stream.format_type = 0x1406
    position_stream.components_count = 3
    position_stream.vert_offset = 0

    texcoord_stream = VertexStream()
    interleaved_vertex_stream.vertex_streams.add(texcoord_stream)
    texcoord_stream.usage = 4
    texcoord_stream.flags = 0
    texcoord_stream.format_type = 0x1406
    texcoord_stream.components_count = 2
    texcoord_stream.vert_offset = 12

    skeleton = SOBJSkeleton()
    cmdl.skeleton = skeleton
    skeleton.flags = 2
    bone = Bone()
    skeleton.bones.add('banner', bone)
    skeleton.root_bone = bone
    bone.name = 'banner'
    bone.flags = 476
    bone.position = Vector3(0, 1, 0)
    bone.local.columns[1].w = 1
    bone.inverse_base.columns[1].w = -1
    bone.billboard_mode = 5

    mtob = MTOB()
    cmdl.materials.add('mt_banner', mtob)
    mtob.name = 'mt_banner'
    mtob.transluscency_kind = 1
    mtob.material_color.specular[0] = ColorFloat(1, 1, 1, 0)
    for i in range(6):
        mtob.material_color.constant[i] = ColorFloat(0, 0, 0, 1)
    mtob.used_texture_coordinates_count = 1
    ref_tex = ReferenceTexture(txob)
    mtob.texture_mappers[0] = TexInfo(ref_tex)
    mtob.texture_mappers[0].sampler.min_filter = 1

    mtob.fragment_shader.texture_combiners[0].src_rgb = 0xe30
    mtob.fragment_shader.texture_combiners[0].src_alpha = 0xe30
    mtob.fragment_shader.texture_combiners[0].combine_rgb = 1
    mtob.fragment_shader.texture_combiners[0].combine_alpha = 1

    return cgfx

def write(cgfx: CGFX) -> bytes:
    strings = StringTable()
    imag = StringTable()
    offset = cgfx.prepare(0, strings, imag)
    offset += -offset % 8 # align to 8 bytes
    offset = strings.prepare(offset)
    cgfx.data.section_size = offset - cgfx.data.offset
    if not imag.empty():
        cgfx.header.nr_blocks = 2
        offset += 8 # IMAG header
    offset = imag.prepare(offset)
    cgfx.header.file_size = offset
    data = cgfx.write(strings, imag)
    data += strings.write()
    if not imag.empty():
        data += b'IMAG' + imag.size().to_bytes(4, 'little') + imag.write()
    return data

if __name__ == '__main__':
    cgfx = make_demo_cgfx()
    with open("test.cgfx", "wb") as f:
        f.write(write(cgfx))