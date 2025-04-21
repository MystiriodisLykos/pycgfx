from dict import DictInfo
from shared import Signature, StandardObject, Vector3, Vector4, Matrix, List
from sobj import SOBJMesh, SOBJShape, SOBJSkeleton
from struct import Struct
from mtob import MTOB


class AnimationGroupMember(StandardObject):
    type = 0
    path: str = None
    member: str = None
    blend_operation_index: str = None
    object_type = 0
    member_type = 0
    res_material_ptr = 0
    subtype = 0
    some_bool = 0
    string = ''
    tex_mapper = 0
    number = 0
    def refresh_struct(self):
        # padding is used at runtime
        fmt = 'Iiiiiiiiixxxxi'
        if self.subtype <= 5:
            fmt += 'i'
        self.struct = Struct(fmt)
    def values(self):
        return (self.type, self.path, self.member, self.blend_operation_index,
            self.object_type, self.member_type, self.res_material_ptr, self.subtype,
            self.some_bool) + ((self.string, self.tex_mapper) if self.subtype <= 5 else (self.number,))
    

class GraphicsAnimationGroup(StandardObject):
    struct = Struct('Iiiiiiiii')
    type = 0x80000000
    flags = 0
    name = ''
    member_type = 0
    members: DictInfo[AnimationGroupMember]
    blend_operations: List[int]
    evalution_timing = 0
    def __init__(self):
        self.members = DictInfo()
        self.blend_operations = List()
    def values(self):
        return (self.type, self.flags, self.name, self.member_type, self.members,
            self.blend_operations, self.evalution_timing)

class CMDL(StandardObject):
    struct = Struct('i4siiiiiiixxxxiifffffffff' + 'f' * 12 * 2 + 'i' * 11)
    type = 0x40000012
    signature = Signature('CMDL')
    revision = 0x7000000
    name = ''
    user_data: DictInfo
    flags = 1
    branch_visible = False
    nr_children = 0
    animation_group_descriptions: DictInfo[GraphicsAnimationGroup]
    scale: Vector3
    rotation: Vector3
    translation: Vector3
    local: Matrix
    world: Matrix
    meshes: List[SOBJMesh]
    materials: DictInfo[MTOB]
    shapes: List[SOBJShape]
    mesh_nodes: DictInfo
    flags2 = 0
    cull_mode = 0
    layer_id = 0
    def __init__(self) -> None:
        super().__init__()
        self.scale = Vector3(1, 1, 1)
        self.rotation = Vector3(0, 0, 0)
        self.translation = Vector3(0, 0, 0)
        self.local = Matrix(Vector4(1, 0, 0, 0), Vector4(0, 1, 0, 0), Vector4(0, 0, 1, 0))
        self.world = Matrix(Vector4(1, 0, 0, 0), Vector4(0, 1, 0, 0), Vector4(0, 0, 1, 0))
        self.user_data = DictInfo()
        self.animation_group_descriptions = DictInfo()
        self.meshes = List()
        self.materials = DictInfo()
        self.shapes = List()
        self.mesh_nodes = DictInfo()
    def values(self) -> tuple:
        return (self.type, self.signature, self.revision, self.name, self.user_data,
                self.flags, self.branch_visible, self.nr_children, self.animation_group_descriptions,
                self.scale, self.rotation, self.translation, self.local, self.world,
                self.meshes, self.materials, self.shapes, self.mesh_nodes, self.flags2, self.cull_mode, self.layer_id)

class CMDLWithSkeleton(CMDL):
    struct = Struct(CMDL.struct.format + 'i')
    type = CMDL.type | 0x80
    skeleton: SOBJSkeleton = None
    def values(self) -> tuple:
        return super().values() + (self.skeleton,)