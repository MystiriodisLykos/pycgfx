from cgfx import CGFX
from cmdl import CMDL, CMDLWithSkeleton
from shared import StringTable, Vector3
from txob import ImageTexture, PixelBasedImage, ReferenceTexture
from sobj import SOBJMesh, SOBJShape, SOBJSkeleton, Bone, BillboardMode
from primitives import Primitive, PrimitiveSet, InterleavedVertexStream, IndexStream, VertexStream, VertexAttributeUsage, VertexAttributeFlags, DataType
from mtob import MTOB, ColorFloat, TexInfo, PicaCommand, LinkedShader, LightingLookupTable
from animation import GraphicsAnimationGroup, AnimationGroupMember, AnimationGroupMemberType
from luts import LUTS
from cflt import CFLT
import swizzler
from PIL import Image

def make_material_animation(material_animation: GraphicsAnimationGroup, mat_name: str):
    member = AnimationGroupMember()
    material_animation.members.add(f'Materials["{mat_name}"].MaterialColor.Emission', member)
    member.object_type = AnimationGroupMemberType.MaterialColor
    member.path = f'Materials["{mat_name}"].MaterialColor.Emission'
    member.member = mat_name
    member.blend_operation_index = 'MaterialColor'
    member.value_offset = 16 * 0
    member.value_size = 16
    member.field_type = 1
    member.parent_name = mat_name
    
    member = AnimationGroupMember()
    material_animation.members.add(f'Materials["{mat_name}"].MaterialColor.Ambient', member)
    member.object_type = AnimationGroupMemberType.MaterialColor
    member.path = f'Materials["{mat_name}"].MaterialColor.Ambient'
    member.member = mat_name
    member.blend_operation_index = 'MaterialColor'
    member.value_offset = 16 * 1
    member.value_size = 16
    member.field_type = 1
    member.value_index = 1
    member.parent_name = mat_name
    
    member = AnimationGroupMember()
    material_animation.members.add(f'Materials["{mat_name}"].MaterialColor.Diffuse', member)
    member.object_type = AnimationGroupMemberType.MaterialColor
    member.path = f'Materials["{mat_name}"].MaterialColor.Diffuse'
    member.member = mat_name
    member.blend_operation_index = 'MaterialColor'
    member.value_offset = 16 * 2
    member.value_size = 16
    member.field_type = 1
    member.value_index = 2
    member.parent_name = mat_name
    
    member = AnimationGroupMember()
    material_animation.members.add(f'Materials["{mat_name}"].MaterialColor.Specular0', member)
    member.object_type = AnimationGroupMemberType.MaterialColor
    member.path = f'Materials["{mat_name}"].MaterialColor.Specular0'
    member.member = mat_name
    member.blend_operation_index = 'MaterialColor'
    member.value_offset = 16 * 3
    member.value_size = 16
    member.field_type = 1
    member.value_index = 3
    member.parent_name = mat_name
    
    member = AnimationGroupMember()
    material_animation.members.add(f'Materials["{mat_name}"].MaterialColor.Specular1', member)
    member.object_type = AnimationGroupMemberType.MaterialColor
    member.path = f'Materials["{mat_name}"].MaterialColor.Specular1'
    member.member = mat_name
    member.blend_operation_index = 'MaterialColor'
    member.value_offset = 16 * 4
    member.value_size = 16
    member.field_type = 1
    member.value_index = 4
    member.parent_name = mat_name
    
    member = AnimationGroupMember()
    material_animation.members.add(f'Materials["{mat_name}"].MaterialColor.Constant0', member)
    member.object_type = AnimationGroupMemberType.MaterialColor
    member.path = f'Materials["{mat_name}"].MaterialColor.Constant0'
    member.member = mat_name
    member.blend_operation_index = 'MaterialColor'
    member.value_offset = 16 * 5
    member.value_size = 16
    member.field_type = 1
    member.value_index = 5
    member.parent_name = mat_name
    
    member = AnimationGroupMember()
    material_animation.members.add(f'Materials["{mat_name}"].MaterialColor.Constant1', member)
    member.object_type = AnimationGroupMemberType.MaterialColor
    member.path = f'Materials["{mat_name}"].MaterialColor.Constant1'
    member.member = mat_name
    member.blend_operation_index = 'MaterialColor'
    member.value_offset = 16 * 6
    member.value_size = 16
    member.field_type = 1
    member.value_index = 6
    member.parent_name = mat_name
    
    member = AnimationGroupMember()
    material_animation.members.add(f'Materials["{mat_name}"].MaterialColor.Constant2', member)
    member.object_type = AnimationGroupMemberType.MaterialColor
    member.path = f'Materials["{mat_name}"].MaterialColor.Constant2'
    member.member = mat_name
    member.blend_operation_index = 'MaterialColor'
    member.value_offset = 16 * 7
    member.value_size = 16
    member.field_type = 1
    member.value_index = 7
    member.parent_name = mat_name
    
    member = AnimationGroupMember()
    material_animation.members.add(f'Materials["{mat_name}"].MaterialColor.Constant3', member)
    member.object_type = AnimationGroupMemberType.MaterialColor
    member.path = f'Materials["{mat_name}"].MaterialColor.Constant3'
    member.member = mat_name
    member.blend_operation_index = 'MaterialColor'
    member.value_offset = 16 * 8
    member.value_size = 16
    member.field_type = 1
    member.value_index = 8
    member.parent_name = mat_name
    
    member = AnimationGroupMember()
    material_animation.members.add(f'Materials["{mat_name}"].MaterialColor.Constant4', member)
    member.object_type = AnimationGroupMemberType.MaterialColor
    member.path = f'Materials["{mat_name}"].MaterialColor.Constant4'
    member.member = mat_name
    member.blend_operation_index = 'MaterialColor'
    member.value_offset = 16 * 9
    member.value_size = 16
    member.field_type = 1
    member.value_index = 9
    member.parent_name = mat_name
    
    member = AnimationGroupMember()
    material_animation.members.add(f'Materials["{mat_name}"].MaterialColor.Constant5', member)
    member.object_type = AnimationGroupMemberType.MaterialColor
    member.path = f'Materials["{mat_name}"].MaterialColor.Constant5'
    member.member = mat_name
    member.blend_operation_index = 'MaterialColor'
    member.value_offset = 16 * 10
    member.value_size = 16
    member.field_type = 1
    member.value_index = 10
    member.parent_name = mat_name
    
    member = AnimationGroupMember()
    material_animation.members.add(f'Materials["{mat_name}"].TextureMappers[0].Sampler.BorderColor', member)
    member.object_type = AnimationGroupMemberType.TextureSampler
    member.path = f'Materials["{mat_name}"].TextureMappers[0].Sampler.BorderColor'
    member.member = mat_name
    member.blend_operation_index = 'TextureMappers[0].Sampler'
    member.value_offset = 12
    member.value_size = 16
    member.field_type = 2
    member.value_index = 0
    member.parent_name = mat_name
    
    member = AnimationGroupMember()
    material_animation.members.add(f'Materials["{mat_name}"].TextureMappers[0].Texture', member)
    member.object_type = AnimationGroupMemberType.TextureMapper
    member.path = f'Materials["{mat_name}"].TextureMappers[0].Texture'
    member.member = mat_name
    member.blend_operation_index = 'TextureMappers[0]'
    member.value_offset = 8
    member.value_size = 4
    member.unknown = 1
    member.field_type = 3
    member.value_index = 0
    member.parent_name = mat_name
    
    member = AnimationGroupMember()
    material_animation.members.add(f'Materials["{mat_name}"].FragmentOperation.BlendOperation.BlendColor', member)
    member.object_type = AnimationGroupMemberType.BlendOperation
    member.path = f'Materials["{mat_name}"].FragmentOperation.BlendOperation.BlendColor'
    member.member = mat_name
    member.blend_operation_index = 'FragmentOperation.BlendOperation'
    member.value_offset = 4
    member.value_size = 16
    member.field_type = 4
    member.value_index = 0
    member.parent_name = mat_name
    
    member = AnimationGroupMember()
    material_animation.members.add(f'Materials["{mat_name}"].TextureCoordinators[0].Scale', member)
    member.object_type = AnimationGroupMemberType.TextureCoordinator
    member.path = f'Materials["{mat_name}"].FragmentOperation.TextureCoordinators[0].Scale'
    member.member = mat_name
    member.blend_operation_index = 'TextureCoordinators[0]'
    member.value_offset = 16
    member.value_size = 8
    member.unknown = 2
    member.field_type = 5
    member.value_index = 0
    member.parent_name = mat_name
    
    member = AnimationGroupMember()
    material_animation.members.add(f'Materials["{mat_name}"].TextureCoordinators[0].Rotate', member)
    member.object_type = AnimationGroupMemberType.TextureCoordinator
    member.path = f'Materials["{mat_name}"].FragmentOperation.TextureCoordinators[0].Rotate'
    member.member = mat_name
    member.blend_operation_index = 'TextureCoordinators[0]'
    member.value_offset = 24
    member.value_size = 4
    member.unknown = 3
    member.field_type = 5
    member.value_index = 1
    member.parent_name = mat_name
    
    member = AnimationGroupMember()
    material_animation.members.add(f'Materials["{mat_name}"].TextureCoordinators[0].Translate', member)
    member.object_type = AnimationGroupMemberType.TextureCoordinator
    member.path = f'Materials["{mat_name}"].FragmentOperation.TextureCoordinators[0].Translate'
    member.member = mat_name
    member.blend_operation_index = 'TextureCoordinators[0]'
    member.value_offset = 28
    member.value_size = 8
    member.unknown = 2
    member.field_type = 5
    member.value_index = 2
    member.parent_name = mat_name

def make_demo_cgfx() -> CGFX:
    cgfx = CGFX()
    txob = swizzler.to_txob(Image.open("banner.png"))
    cgfx.data.textures.add("COMMON1", txob)
    txob.name = 'COMMON1'

    cmdl = CMDLWithSkeleton()
    cgfx.data.models.add("COMMON", cmdl)
    cmdl.name = "COMMON"
    cmdl.flags = 1
    cmdl.branch_visible = True
    cmdl.visible = True

    skeletal_animation = GraphicsAnimationGroup()
    cmdl.animation_group_descriptions.add("SkeletalAnimation", skeletal_animation)
    skeletal_animation.flags = 1
    skeletal_animation.name = 'SkeletalAnimation'
    skeletal_animation.member_type = 1
    skeletal_animation.blend_operations.add(8)
    skeletal_animation.evalution_timing = 1

    banner = AnimationGroupMember()
    skeletal_animation.members.add('banner', banner)
    banner.object_type = AnimationGroupMemberType.Bone
    banner.path = 'banner'
    banner.member = 'banner'
    banner.field_type = 0
    banner.parent_name = 'banner'
    
    visibility_animation = GraphicsAnimationGroup()
    cmdl.animation_group_descriptions.add("VisibilityAnimation", visibility_animation)
    visibility_animation.name = 'VisibilityAnimation'
    visibility_animation.member_type = 3
    visibility_animation.blend_operations.add(0)

    is_visible = AnimationGroupMember()
    visibility_animation.members.add('IsVisible', is_visible)
    is_visible.object_type = AnimationGroupMemberType.Model
    is_visible.path = 'IsVisible'
    is_visible.value_offset = 212
    is_visible.value_size = 1
    is_visible.field_type = 6
    is_visible.value_index = 1

    meshes_zero_is_visible = AnimationGroupMember()
    visibility_animation.members.add('Meshes[0].IsVisible', meshes_zero_is_visible)
    meshes_zero_is_visible.object_type = AnimationGroupMemberType.Mesh
    meshes_zero_is_visible.path = 'Meshes[0].IsVisible'
    meshes_zero_is_visible.member = '0'
    meshes_zero_is_visible.value_offset = 36
    meshes_zero_is_visible.value_size = 1
    meshes_zero_is_visible.field_type = 7
    meshes_zero_is_visible.parent_index = 0

    material_animation = GraphicsAnimationGroup()
    cmdl.animation_group_descriptions.add("MaterialAnimation", material_animation)
    material_animation.name = 'MaterialAnimation'
    material_animation.member_type = 2
    material_animation.evalution_timing = 1
    material_animation.blend_operations.add(3)
    material_animation.blend_operations.add(7)
    material_animation.blend_operations.add(5)
    material_animation.blend_operations.add(2)

    make_material_animation(material_animation, 'mt_banner')

    mesh = SOBJMesh(cmdl)
    cmdl.meshes.add(mesh)
    mesh.mesh_node_visibility_index = 65535
    mesh.material_index = 0
    mesh.shape_index = 0

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
    index_stream.data_type = DataType.UByte
    index_stream.primitive_mode = 0
    index_stream.face_data = bytes([0, 1, 2, 1, 3, 2])
    primitive.buffer_objects.add(0)
    primitive.flags = 8
    
    interleaved_vertex_stream = InterleavedVertexStream()
    shape.vertex_attributes.add(interleaved_vertex_stream)
    interleaved_vertex_stream.usage = VertexAttributeUsage.Interlave
    interleaved_vertex_stream.flags = VertexAttributeFlags.Interleave
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
    position_stream.usage = VertexAttributeUsage.Position
    position_stream.flags = 0
    position_stream.format_type = DataType.Float
    position_stream.components_count = 3
    position_stream.vert_offset = 0

    texcoord_stream = VertexStream()
    interleaved_vertex_stream.vertex_streams.add(texcoord_stream)
    texcoord_stream.usage = VertexAttributeUsage.TextureCoordinate0
    texcoord_stream.flags = 0
    texcoord_stream.format_type = DataType.Float
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
    bone.position = Vector3(10, 1, 0)
    bone.local.columns[1].w = 1
    bone.inverse_base.columns[1].w = -1
    bone.billboard_mode = BillboardMode.YAxial

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