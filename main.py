from cgfx import CGFX
from cmdl import CMDL, CMDLWithSkeleton
from shared import StringTable, Vector3, Vector4
from dict import DictInfo
from txob import ImageTexture, PixelBasedImage, ReferenceTexture
from sobj import SOBJMesh, SOBJShape, SOBJSkeleton, Bone, BillboardMode, BoneFlag, SkeletonFlag
from primitives import Primitive, PrimitiveSet, InterleavedVertexStream, IndexStream, VertexStream, VertexAttributeUsage, VertexAttributeFlag, DataType, VertexParamAttribute
from mtob import MTOB, ColorFloat, TexInfo, PicaCommand, LinkedShader, LightingLookupTable, MTOBFlag, ConstantColorSource, BumpMode
from animation import GraphicsAnimationGroup, AnimationGroupMember, AnimationGroupMemberType
from luts import LUTS, LutTable
from cenv import CENV, CENVLight, CENVLightSet
from cflt import CFLT
import swizzler
from PIL import Image
import gltflib
from io import BytesIO
import math

def quat_to_euler(x: float, y: float, z: float, w: float) -> Vector3:
    t0 = 2 * (w * x + y * z)
    t1 = 1 - 2 * (x * x + y * y)
    ex = math.atan2(t0, t1)

    t2 = max(-1, min(1, 2 * (w * y - z * x)))
    ey = math.asin(t2)

    t3 = 2 * (w * z + x * y)
    t4 = 1 - 2 * (y * y + z * z)
    ez = math.atan2(t3, t4)

    return Vector3(ex, ey, ez)

def make_material_animation(material_animation: GraphicsAnimationGroup, mtob: MTOB):
    member = AnimationGroupMember()
    material_animation.members.add(f'Materials["{mtob.name}"].MaterialColor.Emission', member)
    member.object_type = AnimationGroupMemberType.MaterialColor
    member.path = f'Materials["{mtob.name}"].MaterialColor.Emission'
    member.member = mtob.name
    member.blend_operation_index = 'MaterialColor'
    member.value_offset = 16 * 0
    member.value_size = 16
    member.field_type = 1
    member.parent_name = mtob.name
    
    member = AnimationGroupMember()
    material_animation.members.add(f'Materials["{mtob.name}"].MaterialColor.Ambient', member)
    member.object_type = AnimationGroupMemberType.MaterialColor
    member.path = f'Materials["{mtob.name}"].MaterialColor.Ambient'
    member.member = mtob.name
    member.blend_operation_index = 'MaterialColor'
    member.value_offset = 16 * 1
    member.value_size = 16
    member.field_type = 1
    member.value_index = 1
    member.parent_name = mtob.name
    
    member = AnimationGroupMember()
    material_animation.members.add(f'Materials["{mtob.name}"].MaterialColor.Diffuse', member)
    member.object_type = AnimationGroupMemberType.MaterialColor
    member.path = f'Materials["{mtob.name}"].MaterialColor.Diffuse'
    member.member = mtob.name
    member.blend_operation_index = 'MaterialColor'
    member.value_offset = 16 * 2
    member.value_size = 16
    member.field_type = 1
    member.value_index = 2
    member.parent_name = mtob.name
    
    member = AnimationGroupMember()
    material_animation.members.add(f'Materials["{mtob.name}"].MaterialColor.Specular0', member)
    member.object_type = AnimationGroupMemberType.MaterialColor
    member.path = f'Materials["{mtob.name}"].MaterialColor.Specular0'
    member.member = mtob.name
    member.blend_operation_index = 'MaterialColor'
    member.value_offset = 16 * 3
    member.value_size = 16
    member.field_type = 1
    member.value_index = 3
    member.parent_name = mtob.name
    
    member = AnimationGroupMember()
    material_animation.members.add(f'Materials["{mtob.name}"].MaterialColor.Specular1', member)
    member.object_type = AnimationGroupMemberType.MaterialColor
    member.path = f'Materials["{mtob.name}"].MaterialColor.Specular1'
    member.member = mtob.name
    member.blend_operation_index = 'MaterialColor'
    member.value_offset = 16 * 4
    member.value_size = 16
    member.field_type = 1
    member.value_index = 4
    member.parent_name = mtob.name
    
    member = AnimationGroupMember()
    material_animation.members.add(f'Materials["{mtob.name}"].MaterialColor.Constant0', member)
    member.object_type = AnimationGroupMemberType.MaterialColor
    member.path = f'Materials["{mtob.name}"].MaterialColor.Constant0'
    member.member = mtob.name
    member.blend_operation_index = 'MaterialColor'
    member.value_offset = 16 * 5
    member.value_size = 16
    member.field_type = 1
    member.value_index = 5
    member.parent_name = mtob.name
    
    member = AnimationGroupMember()
    material_animation.members.add(f'Materials["{mtob.name}"].MaterialColor.Constant1', member)
    member.object_type = AnimationGroupMemberType.MaterialColor
    member.path = f'Materials["{mtob.name}"].MaterialColor.Constant1'
    member.member = mtob.name
    member.blend_operation_index = 'MaterialColor'
    member.value_offset = 16 * 6
    member.value_size = 16
    member.field_type = 1
    member.value_index = 6
    member.parent_name = mtob.name
    
    member = AnimationGroupMember()
    material_animation.members.add(f'Materials["{mtob.name}"].MaterialColor.Constant2', member)
    member.object_type = AnimationGroupMemberType.MaterialColor
    member.path = f'Materials["{mtob.name}"].MaterialColor.Constant2'
    member.member = mtob.name
    member.blend_operation_index = 'MaterialColor'
    member.value_offset = 16 * 7
    member.value_size = 16
    member.field_type = 1
    member.value_index = 7
    member.parent_name = mtob.name
    
    member = AnimationGroupMember()
    material_animation.members.add(f'Materials["{mtob.name}"].MaterialColor.Constant3', member)
    member.object_type = AnimationGroupMemberType.MaterialColor
    member.path = f'Materials["{mtob.name}"].MaterialColor.Constant3'
    member.member = mtob.name
    member.blend_operation_index = 'MaterialColor'
    member.value_offset = 16 * 8
    member.value_size = 16
    member.field_type = 1
    member.value_index = 8
    member.parent_name = mtob.name
    
    member = AnimationGroupMember()
    material_animation.members.add(f'Materials["{mtob.name}"].MaterialColor.Constant4', member)
    member.object_type = AnimationGroupMemberType.MaterialColor
    member.path = f'Materials["{mtob.name}"].MaterialColor.Constant4'
    member.member = mtob.name
    member.blend_operation_index = 'MaterialColor'
    member.value_offset = 16 * 9
    member.value_size = 16
    member.field_type = 1
    member.value_index = 9
    member.parent_name = mtob.name
    
    member = AnimationGroupMember()
    material_animation.members.add(f'Materials["{mtob.name}"].MaterialColor.Constant5', member)
    member.object_type = AnimationGroupMemberType.MaterialColor
    member.path = f'Materials["{mtob.name}"].MaterialColor.Constant5'
    member.member = mtob.name
    member.blend_operation_index = 'MaterialColor'
    member.value_offset = 16 * 10
    member.value_size = 16
    member.field_type = 1
    member.value_index = 10
    member.parent_name = mtob.name
    
    for i in range(len(mtob.texture_mappers)):
        if mtob.texture_mappers[i] is None:
            continue

        member = AnimationGroupMember()
        material_animation.members.add(f'Materials["{mtob.name}"].TextureMappers[{i}].Sampler.BorderColor', member)
        member.object_type = AnimationGroupMemberType.TextureSampler
        member.path = f'Materials["{mtob.name}"].TextureMappers[{i}].Sampler.BorderColor'
        member.member = mtob.name
        member.blend_operation_index = f'TextureMappers[{i}].Sampler'
        member.value_offset = 12
        member.value_size = 16
        member.field_type = 2
        member.field_index = i
        member.value_index = 0
        member.parent_name = mtob.name
        
        member = AnimationGroupMember()
        material_animation.members.add(f'Materials["{mtob.name}"].TextureMappers[{i}].Texture', member)
        member.object_type = AnimationGroupMemberType.TextureMapper
        member.path = f'Materials["{mtob.name}"].TextureMappers[{i}].Texture'
        member.member = mtob.name
        member.blend_operation_index = f'TextureMappers[{i}]'
        member.value_offset = 8
        member.value_size = 4
        member.unknown = 1
        member.field_type = 3
        member.field_index = i
        member.value_index = 0
        member.parent_name = mtob.name
    
        member = AnimationGroupMember()
        material_animation.members.add(f'Materials["{mtob.name}"].TextureCoordinators[{i}].Scale', member)
        member.object_type = AnimationGroupMemberType.TextureCoordinator
        member.path = f'Materials["{mtob.name}"].FragmentOperation.TextureCoordinators[{i}].Scale'
        member.member = mtob.name
        member.blend_operation_index = f'TextureCoordinators[{i}]'
        member.value_offset = 16
        member.value_size = 8
        member.unknown = 2
        member.field_type = 5
        member.field_index = i
        member.value_index = 0
        member.parent_name = mtob.name
        
        member = AnimationGroupMember()
        material_animation.members.add(f'Materials["{mtob.name}"].TextureCoordinators[{i}].Rotate', member)
        member.object_type = AnimationGroupMemberType.TextureCoordinator
        member.path = f'Materials["{mtob.name}"].FragmentOperation.TextureCoordinators[{i}].Rotate'
        member.member = mtob.name
        member.blend_operation_index = f'TextureCoordinators[{i}]'
        member.value_offset = 24
        member.value_size = 4
        member.unknown = 3
        member.field_type = 5
        member.field_index = i
        member.value_index = 1
        member.parent_name = mtob.name
        
        member = AnimationGroupMember()
        material_animation.members.add(f'Materials["{mtob.name}"].TextureCoordinators[{i}].Translate', member)
        member.object_type = AnimationGroupMemberType.TextureCoordinator
        member.path = f'Materials["{mtob.name}"].FragmentOperation.TextureCoordinators[{i}].Translate'
        member.member = mtob.name
        member.blend_operation_index = f'TextureCoordinators[{i}]'
        member.value_offset = 28
        member.value_size = 8
        member.unknown = 2
        member.field_type = 5
        member.field_index = i
        member.value_index = 2
        member.parent_name = mtob.name
    
    member = AnimationGroupMember()
    material_animation.members.add(f'Materials["{mtob.name}"].FragmentOperation.BlendOperation.BlendColor', member)
    member.object_type = AnimationGroupMemberType.BlendOperation
    member.path = f'Materials["{mtob.name}"].FragmentOperation.BlendOperation.BlendColor'
    member.member = mtob.name
    member.blend_operation_index = 'FragmentOperation.BlendOperation'
    member.value_offset = 4
    member.value_size = 16
    member.field_type = 4
    member.value_index = 0
    member.parent_name = mtob.name

def gltf_get_bv_data(gltf: gltflib.GLTF, bv_id: int) -> bytes:
    bv = gltf.model.bufferViews[bv_id]
    buf = gltf.model.buffers[bv.buffer]
    if buf.uri is None:
        buf_res = gltf.get_glb_resource()
    else:
        buf_res = gltf.get_resource(buf.uri)
    return buf_res.data[bv.byteOffset:bv.byteOffset+bv.byteLength]

def gltf_get_texture(cgfx: CGFX, gltf: gltflib.GLTF, image_id: int, normal: bool = False) -> ImageTexture:
    image = gltf.model.images[image_id]
    tex_name = image.name or image.uri or f'image{image_id}'
    if normal: tex_name = f'NORM~{tex_name}'
    if tex_name in cgfx.data.textures:
        return cgfx.data.textures.get(tex_name)

    if image.uri is not None:
        image_data = gltf.get_resource(image.uri).data
    elif image.bufferView is not None:
        image_data = gltf_get_bv_data(gltf, image.bufferView)

    im: Image.Image = Image.open(BytesIO(image_data))
    if im.width > 256: im = im.resize((256, im.height))
    if im.height > 256: im = im.resize((im.width, 256))
    if normal:
        im = im.convert('RGBA')
        for x in range(im.width):
            for y in range(im.height):
                px = im.getpixel((x, y))
                im.putpixel((x, y), (255 - px[0], 255 - px[1], px[2]))
    txob = swizzler.to_txob(im.transpose(Image.Transpose.FLIP_TOP_BOTTOM))
    txob.name = tex_name
    cgfx.data.textures.add(tex_name, txob)
    return txob

def make_bones(gltf: gltflib.GLTF, node_ids: list[int], bone_dict: DictInfo[Bone]) -> list[Bone]:
    bones = []
    for node_id in node_ids:
        node = gltf.model.nodes[node_id]
        bone = Bone()
        bone.name = node.name
        bone_dict.add(bone.name, bone)
        bone.joint_id = node_id
        bone.flags = BoneFlag.IsNeedRendering | BoneFlag.IsLocalMatrixCalculate | BoneFlag.IsWorldMatrixCalculate
        if bones:
            bone.previous_sibling = bones[-1]
            bones[-1].next_sibling = bone
        bones.append(bone)

        if node.translation:
            bone.position = Vector3(*node.translation)
        if node.scale:
            bone.scale = Vector3(*node.scale)
        if node.rotation:
            bone.rotation = quat_to_euler(*node.rotation)
        
        if bone.position == Vector3(0, 0, 0):
            bone.flags |= BoneFlag.IsTranslateZero
        if bone.scale == Vector3(1, 1, 1):
            bone.flags |= BoneFlag.IsScaleOne
        if bone.scale.x == bone.scale.y == bone.scale.z:
            bone.flags |= BoneFlag.IsUniformScale
        if bone.rotation == Vector3(0, 0, 0):
            bone.flags |= BoneFlag.IsRotateZero
        
        all_flags = BoneFlag.IsTranslateZero | BoneFlag.IsRotateZero | BoneFlag.IsScaleOne
        if (bone.flags & all_flags) == all_flags:
            bone.flags |= BoneFlag.IsIdentity
        
        if node.children:
            child_bones = make_bones(gltf, node.children, bone_dict)
            if child_bones:
                bone.child = child_bones[0]
                for c in child_bones:
                    c.parent = bone
    return bones

def convert_gltf(gltf: gltflib.GLTF) -> CGFX:
    default_sampler = gltflib.Sampler(magFilter=9729, minFilter=9729, wrapS=10497, wrapT=10497)
    default_material = gltflib.Material(name='glTF default material')

    cgfx = CGFX()

    cmdl = CMDLWithSkeleton()
    cgfx.data.models.add("COMMON", cmdl)
    cmdl.name = "COMMON"

    cmdl.skeleton = SOBJSkeleton()
    node_ids = gltf.model.scenes[gltf.model.scene].nodes
    root_bone = Bone()
    root_bone.name = 'Scene root'
    # ensure name is unique
    while any(n.name == root_bone.name for n in gltf.model.nodes):
        root_bone.name += '_'
    root_bone.joint_id = len(gltf.model.nodes)
    root_bone.flags = BoneFlag.IsIdentity | BoneFlag.IsNeedRendering
    cmdl.skeleton.root_bone = root_bone
    cmdl.skeleton.bones.add(root_bone.name, root_bone)
    initial_bones = make_bones(gltf, node_ids, cmdl.skeleton.bones)

    # clean up joint ids
    node_to_bone = {}
    bone_to_node = {}

    for b in cmdl.skeleton.bones:
        bone = cmdl.skeleton.bones.get(b)
        if bone.joint_id >= 0:
            bone_to_node[cmdl.skeleton.bones.get_index(b)] = bone.joint_id
            node_to_bone[bone.joint_id] = cmdl.skeleton.bones.get_index(b)
            bone.joint_id = cmdl.skeleton.bones.get_index(b)

    for b in initial_bones:
        b.parent = root_bone
    root_bone.child = initial_bones[0]

    for b in cmdl.skeleton.bones:
        bone = cmdl.skeleton.bones.get(b)
        if bone.parent:
            bone.parent_id = bone.parent.joint_id

    mesh_nodes = [
        bone_to_node[cmdl.skeleton.bones.get(bone_name).joint_id]
        for bone_name in cmdl.skeleton.bones
        if bone_to_node[cmdl.skeleton.bones.get(bone_name).joint_id] < len(gltf.model.nodes)
            and gltf.model.nodes[bone_to_node[cmdl.skeleton.bones.get(bone_name).joint_id]].mesh is not None]
    
    for node_id in mesh_nodes:
        mesh = gltf.model.meshes[gltf.model.nodes[node_id].mesh]
        
        for material in (gltf.model.materials[p.material] if p.material is not None else default_material for p in mesh.primitives):
            if material.name not in cmdl.materials:
                mtob = MTOB()
                cmdl.materials.add(material.name, mtob)
                mtob.name = material.name
                # multiply base texture with primary color
                mtob.fragment_shader.texture_combiners[0].src_rgb = 0x030
                mtob.fragment_shader.texture_combiners[0].src_alpha = 0x030
                mtob.fragment_shader.texture_combiners[0].combine_rgb = 1
                mtob.fragment_shader.texture_combiners[0].combine_alpha = 1
                # multiply with diffuse lighting
                mtob.fragment_shader.texture_combiners[1].src_rgb = 0x0f1
                mtob.fragment_shader.texture_combiners[1].combine_rgb = 1
                pmr = material.pbrMetallicRoughness or gltflib.PBRMetallicRoughness()
                base_tex = pmr.baseColorTexture
                if pmr.baseColorFactor:
                    mtob.material_color.diffuse = ColorFloat(*pmr.baseColorFactor)
                mtob.flags = MTOBFlag.FragmentLight
                # mtob.fragment_shader.fragment_lighting_table.distribution_0_sampler = LightingLookupTable()
                # mtob.fragment_shader.fragment_lighting_table.distribution_0_sampler.sampler.binary_path = 'LutSet'
                # mtob.fragment_shader.fragment_lighting_table.distribution_0_sampler.sampler.table_name = 'MyLut'
                if base_tex:
                    tex = gltf.model.textures[base_tex.index]
                    # sampler = gltf.model.samplers[tex.sampler] if tex.sampler is not None else default_sampler
                    tex_info = TexInfo(ReferenceTexture(gltf_get_texture(cgfx, gltf, tex.source, False)))
                    tex_info.sampler.min_filter = 1
                    mtob.texture_mappers[mtob.used_texture_coordinates_count] = tex_info
                    mtob.texture_coordinators[mtob.used_texture_coordinates_count].source_coordinate = base_tex.texCoord or 0
                    mtob.used_texture_coordinates_count += 1
                else:
                    mtob.fragment_shader.texture_combiners[0].combine_rgb = 0
                    mtob.fragment_shader.texture_combiners[0].combine_alpha = 0
                if material.normalTexture:
                    # TODO bump texture needs to be inverted (at least partially)
                    tex = gltf.model.textures[material.normalTexture.index]
                    
                    # sampler = gltf.model.samplers[tex.sampler] if tex.sampler is not None else default_sampler
                    tex_info = TexInfo(ReferenceTexture(gltf_get_texture(cgfx, gltf, tex.source, True)))
                    tex_info.sampler.min_filter = 1
                    mtob.texture_mappers[mtob.used_texture_coordinates_count] = tex_info
                    mtob.texture_coordinators[mtob.used_texture_coordinates_count].source_coordinate = material.normalTexture.texCoord or 0
                    mtob.used_texture_coordinates_count += 1
                    mtob.fragment_shader.fragment_lighting.bump_mode = BumpMode.AsBump
                    mtob.fragment_shader.fragment_lighting.bump_texture = 0
                    mtob.fragment_shader.fragment_lighting.is_bump_renormalize = True
        
        for i, p in enumerate(mesh.primitives):
            sobj_mesh = SOBJMesh(cmdl)
            cmdl.meshes.add(sobj_mesh)
            sobj_mesh.mesh_node_visibility_index = 65535
            sobj_mesh.material_index = cmdl.materials.get_index(gltf.model.materials[p.material].name if p.material is not None else default_material.name)
            sobj_mesh.shape_index = len(cmdl.shapes)
            shape = SOBJShape()
            cmdl.shapes.add(shape)
            primitive_set = PrimitiveSet()
            shape.primitive_sets.add(primitive_set)
            primitive_set.related_bones.add(node_to_bone[node_id])
            primitive = Primitive()
            primitive_set.primitives.add(primitive)
            if p.indices is not None:
                indices = gltf.model.accessors[p.indices]
                index_stream = IndexStream()
                index_stream.data_type = indices.componentType
                index_stream.face_data = gltf_get_bv_data(gltf, indices.bufferView)
                primitive.index_streams.add(index_stream)
                primitive.buffer_objects.add(0)
            for ty, acc_id in p.attributes.__dict__.items():
                if acc_id is None:
                    continue
                acc = gltf.model.accessors[acc_id]
                vs = VertexStream()
                vs.usage = {
                    "POSITION": VertexAttributeUsage.Position,
                    "NORMAL": VertexAttributeUsage.Normal,
                    "TANGENT": VertexAttributeUsage.Tangent,
                    "TEXCOORD_0": VertexAttributeUsage.TextureCoordinate0,
                    "TEXCOORD_1": VertexAttributeUsage.TextureCoordinate1,
                    "COLOR_0": VertexAttributeUsage.Color,
                    "JOINTS_0": VertexAttributeUsage.BoneIndex,
                    "WEIGHTS_0": VertexAttributeUsage.BoneWeight,
                }.get(ty)
                if vs.usage is None: continue
                shape.vertex_attributes.add(vs)
                vs.components_count = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4}[acc.type]
                vs.format_type = acc.componentType
                vs.vertex_stream_data = gltf_get_bv_data(gltf, acc.bufferView)
            # if p.attributes.JOINTS_0 is None:
            #     param = VertexParamAttribute()
            #     param.usage = VertexAttributeUsage.BoneIndex
            #     param.attributes = [0]

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

    for i in range(len(cmdl.meshes)):
        mesh_is_visible = AnimationGroupMember()
        visibility_animation.members.add(f'Meshes[{i}].IsVisible', mesh_is_visible)
        mesh_is_visible.object_type = AnimationGroupMemberType.Mesh
        mesh_is_visible.path = f'Meshes[{i}].IsVisible'
        mesh_is_visible.member = str(i)
        mesh_is_visible.value_offset = 36
        mesh_is_visible.value_size = 1
        mesh_is_visible.field_type = 7
        mesh_is_visible.parent_index = i
    
    skeletal_animation = GraphicsAnimationGroup()
    cmdl.animation_group_descriptions.add("SkeletalAnimation", skeletal_animation)
    skeletal_animation.flags = 1
    skeletal_animation.name = 'SkeletalAnimation'
    skeletal_animation.member_type = 1
    skeletal_animation.blend_operations.add(8)
    skeletal_animation.evalution_timing = 1

    for b in cmdl.skeleton.bones:
        member = AnimationGroupMember()
        skeletal_animation.members.add(b, member)
        member.object_type = AnimationGroupMemberType.Bone
        member.path = b
        member.member = b
        member.field_type = 0
        member.parent_name = b

    material_animation = GraphicsAnimationGroup()
    cmdl.animation_group_descriptions.add("MaterialAnimation", material_animation)
    material_animation.name = 'MaterialAnimation'
    material_animation.member_type = 2
    material_animation.evalution_timing = 1
    material_animation.blend_operations.add(3)
    material_animation.blend_operations.add(7)
    material_animation.blend_operations.add(5)
    material_animation.blend_operations.add(2)

    for m in cmdl.materials:
        make_material_animation(material_animation, cmdl.materials.get(m))

    cenv = CENV()
    cenv.name = 'Scene'
    cgfx.data.scenes.add(cenv.name, cenv)
    light_set = CENVLightSet()
    cenv.light_sets.add(light_set)
    cenv_light = CENVLight()
    light_set.lights.add(cenv_light)
    cenv_light.name = 'TheLight'

    cflt = CFLT()
    cflt.name = 'TheLight'
    cgfx.data.lights.add(cflt.name, cflt)

    # optional lighting stuff

    # light_animation = GraphicsAnimationGroup()
    # light_animation.name = 'LightAnimation'
    # cflt.animation_group_descriptions.add(light_animation.name, light_animation)
    # light_animation.member_type = 4
    # light_animation.blend_operations.add(8)
    # light_animation.blend_operations.add(3)
    # light_animation.blend_operations.add(6)
    # light_animation.blend_operations.add(2)
    # light_animation.blend_operations.add(0)
    
    # member = AnimationGroupMember()
    # light_animation.members.add('Transform', member)
    # member.object_type = 0x800000
    # member.path = 'Transform'
    # member.value_offset = 48
    # member.value_size = 36
    # member.field_type = 9
    # member.parent_index = 9

    # member = AnimationGroupMember()
    # light_animation.members.add('Ambient', member)
    # member.object_type = 0x100000
    # member.path = 'Ambient'
    # member.value_offset = 188
    # member.value_size = 16
    # member.unknown = 1
    # member.field_type = 13
    # member.value_index = 0

    # member = AnimationGroupMember()
    # light_animation.members.add('Diffuse', member)
    # member.object_type = 0x100000
    # member.path = 'Diffuse'
    # member.value_offset = 204
    # member.value_size = 16
    # member.unknown = 1
    # member.field_type = 13
    # member.value_index = 1

    # member = AnimationGroupMember()
    # light_animation.members.add('Specular0', member)
    # member.object_type = 0x100000
    # member.path = 'Specular0'
    # member.value_offset = 220
    # member.value_size = 16
    # member.unknown = 1
    # member.field_type = 13
    # member.value_index = 2

    # member = AnimationGroupMember()
    # light_animation.members.add('Specular1', member)
    # member.object_type = 0x100000
    # member.path = 'Specular1'
    # member.value_offset = 236
    # member.value_size = 16
    # member.unknown = 1
    # member.field_type = 13
    # member.value_index = 3

    # member = AnimationGroupMember()
    # light_animation.members.add('Direction', member)
    # member.object_type = 0x100000
    # member.path = 'Direction'
    # member.value_offset = 268
    # member.value_size = 12
    # member.unknown = 2
    # member.field_type = 13
    # member.value_index = 4

    # member = AnimationGroupMember()
    # light_animation.members.add('DistanceAttenuationStart', member)
    # member.object_type = 0x100000
    # member.path = 'DistanceAttenuationStart'
    # member.value_offset = 288
    # member.value_size = 4
    # member.unknown = 3
    # member.field_type = 13
    # member.value_index = 5

    # member = AnimationGroupMember()
    # light_animation.members.add('DistanceAttenuationEnd', member)
    # member.object_type = 0x100000
    # member.path = 'DistanceAttenuationEnd'
    # member.value_offset = 292
    # member.value_size = 4
    # member.unknown = 3
    # member.field_type = 13
    # member.value_index = 6

    # member = AnimationGroupMember()
    # light_animation.members.add('IsLightEnabled', member)
    # member.object_type = 0x100000
    # member.path = 'IsLightEnabled'
    # member.value_offset = 180
    # member.value_size = 1
    # member.unknown = 4
    # member.field_type = 12

    # luts = LUTS()
    # luts.name = 'LutSet'
    # cgfx.data.lookup_tables.add('LutSet', luts)
    # lut_info = LutTable()
    # lut_info.name = 'MyLut'
    # luts.tables.add('MyLut', lut_info)
    
    return cgfx

        

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
    interleaved_vertex_stream.flags = VertexAttributeFlag.Interleave
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
    bone.position = Vector3(0, 10, 0)
    bone.local.columns[1].w = 1
    bone.inverse_base.columns[1].w = -100
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

    make_material_animation(material_animation, mtob)

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
    if len(data) > 0x80000:
        print(f"WARNING: CGFX is too big ({len(data)} bytes, max is {0x80000} bytes)")
    return data

if __name__ == '__main__':
    # cgfx = make_demo_cgfx()
    gltf = gltflib.GLTF.load("suzanne.glb", load_file_resources=True)
    cgfx = convert_gltf(gltf)
    with open("test.cgfx", "wb") as f:
        f.write(write(cgfx))