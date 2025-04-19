from dict import DictInfo
from shared import Signature, StandardObject, Vector3, Matrix, List
from sobj import SOBJMesh, SOBJShape
from struct import Struct


class CMDL(StandardObject):
    struct = Struct('i4siiiiiiixxxxiifffffffff' + 'f' * 12 * 2 + 'i' * 11)
    type = 0x40000012
    signature = Signature('CMDL')
    revision = 0x9000000
    name: str
    user_data: DictInfo
    flags = 1
    branch_visible = False
    nr_children = 0
    animation_group_descriptions: DictInfo
    scale = Vector3(1, 1, 1)
    rotation = Vector3(0, 0, 0)
    translation = Vector3(0, 0, 0)
    local = Matrix(Vector3(1, 0, 0), Vector3(0, 1, 0), Vector3(0, 0, 1), Vector3(0, 0, 0))
    world = Matrix(Vector3(1, 0, 0), Vector3(0, 1, 0), Vector3(0, 0, 1), Vector3(0, 0, 0))
    meshes: List[SOBJMesh]
    materials: DictInfo
    shapes: List[SOBJShape]
    mesh_nodes: DictInfo
    flags2 = 0
    cull_mode = 0
    layer_id = 0
    def __init__(self) -> None:
        super().__init__()
        self.user_data = DictInfo()
        self.animation_group_descriptions = DictInfo()
        self.meshes = List([SOBJMesh()])
        self.materials = DictInfo()
        self.shapes = List([SOBJShape()])
        self.mesh_nodes = DictInfo()
        self.name = ""
    def values(self) -> tuple:
        return (self.type, self.signature, self.revision, self.name, self.user_data,
                self.flags, self.branch_visible, self.nr_children, self.animation_group_descriptions,
                self.scale, self.rotation, self.translation, self.local, self.world,
                self.meshes, self.materials, self.shapes, self.mesh_nodes, self.flags2, self.cull_mode, self.layer_id)

class CMDLWithSkeleton(CMDL):
    struct = Struct(CMDL.struct.format + 'i')
    type = CMDL.type | 0x80
    skeleton = None
    def values(self) -> tuple:
        return super().values() + (self.skeleton,)