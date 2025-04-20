from struct import Struct

from dict import DictInfo
from shared import Signature, StandardObject, List, Vector3, OrientationMatrix, Reference, Matrix

from primitives import VertexAttribute, PrimitiveSet

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cmdl import CMDL


class SOBJMesh(StandardObject):
    struct = Struct('i4siiiiiii?BH' + 'x' * 4 * 18 + 'i')
    type = 0x1000000
    signature = Signature("SOBJ")
    revision = 0
    name = ''
    user_data: DictInfo
    shape_index = 0
    material_index = 0
    owner: "CMDL"
    is_visible = True
    priority = 0
    mesh_node_visibility_index = 0
    mesh_node_name = ''
    def __init__(self, owner) -> None:
        super().__init__()
        self.user_data = DictInfo()
        self.owner = owner
    def values(self) -> tuple:
        return (self.type, self.signature, self.revision, self.name, self.user_data,
            self.shape_index, self.material_index, Reference(self.owner), self.is_visible,
            self.priority, self.mesh_node_visibility_index, self.mesh_node_name)

class OrientedBoundingBox(StandardObject):
    struct = 'i' + 'f' * (3 + 9 + 3)
    type = 0x80000000
    center_pos: Vector3
    orientation: Matrix
    size: Vector3
    def __init__(self):
        self.center_pos = Vector3(0, 0, 0)
        self.orientation = OrientationMatrix(Vector3(1, 0, 0), Vector3(0, 1, 0), Vector3(0, 0, 1))
        self.size = Vector3(1, 1, 1)
    def values(self) -> tuple:
        return (self.type, self.center_pos, self.orientation, self.size)

class SOBJShape(StandardObject):
    struct = Struct('i4siiiiiifffiiiiii')
    type = 0x10000001
    signature = Signature("SOBJ")
    revision = 0
    name: str
    user_data: DictInfo
    flags = 0
    oriented_bounding_box = 0
    position_offset: Vector3
    primitive_sets: List[PrimitiveSet]
    base_address = 0
    vertex_attributes: List[VertexAttribute]
    blend_shape = 0
    def __init__(self) -> None:
        super().__init__()
        self.user_data = DictInfo()
        self.name = 'shape'
        self.position_offset = Vector3(0, 0, 0)
        self.primitive_sets = List()
        self.vertex_attributes = List()
    def values(self) -> tuple:
        return (self.type, self.signature, self.revision, self.name, self.user_data,
            self.flags, self.oriented_bounding_box, self.position_offset,
            self.primitive_sets, self.base_address, self.vertex_attributes,
            self.blend_shape)

class Bone(StandardObject):
    struct = Struct('iiiiiiiifffffffff' + 'f' * (12*3) + 'ixxxxxxxx')
    name = ''
    flags = 0
    joint_id = 0
    parent_id = -1
    parent = None
    child = None
    previous_sibling = None
    next_sibling = None
    scale: Vector3
    rotation: Vector3
    position: Vector3
    local: Matrix
    world: Matrix
    inverse_base: Matrix
    billboard_mode = 0
    def __init__(self):
        self.scale = Vector3(1, 1, 1)
        self.rotation = Vector3(0, 0, 0)
        self.position = Vector3(0, 0, 0)
        self.local = Matrix(Vector3(1, 0, 0), Vector3(0, 1, 0), Vector3(0, 0, 1), Vector3(0, 0, 0))
        self.world = Matrix(Vector3(1, 0, 0), Vector3(0, 1, 0), Vector3(0, 0, 1), Vector3(0, 0, 0))
        self.inverse_base = Matrix(Vector3(1, 0, 0), Vector3(0, 1, 0), Vector3(0, 0, 1), Vector3(0, 0, 0))

class SOBJSkeleton(StandardObject):
    struct = Struct('i4siiiiiiiii')
    type = 0x2000000
    signature = Signature("SOBJ")
    revision = 0
    name = ''
    user_data: DictInfo
    bones: DictInfo[Bone]
    root_bone = None
    scaling_rule = 0
    flags = 0
    def __init__(self):
        self.user_data = DictInfo()
        self.bones = DictInfo()
    def values(self):
        return (self.type, self.signature, self.revision, self.name, self.user_data,
            self.bones, self.root_bone, self.scaling_rule, self.flags)

