from struct import Struct

from dict import DictInfo
from shared import Signature, StandardObject, List, Vector3, OrientationMatrix, Reference

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
    center_pos = Vector3(0, 0, 0)
    orientation_matrix = OrientationMatrix(Vector3(1, 0, 0), Vector3(0, 1, 0), Vector3(0, 0, 1))
    size = Vector3(1, 1, 1)
    def values(self) -> tuple:
        return (self.type, self.center_pos, self.orientation_matrix, self.size)

class SOBJShape(StandardObject):
    struct = Struct('i4siiiiiifffiiiiii')
    type = 0x10000001
    signature = Signature("SOBJ")
    revision = 0
    name: str
    user_data: DictInfo
    flags = 0
    oriented_bounding_box = 0
    position_offset = Vector3(0, 0, 0)
    primitive_sets: List[PrimitiveSet]
    base_address = 0
    vertex_attributes: List[VertexAttribute]
    blend_shape = 0
    def __init__(self) -> None:
        super().__init__()
        self.user_data = DictInfo()
        self.name = 'shape'
        self.primitive_sets = List()
        self.vertex_attributes = List()
    def values(self) -> tuple:
        return (self.type, self.signature, self.revision, self.name, self.user_data,
            self.flags, self.oriented_bounding_box, self.position_offset,
            self.primitive_sets, self.base_address, self.vertex_attributes,
            self.blend_shape)    
