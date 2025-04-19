from shared import InlineObject, Signature, StandardObject, StringTable
from typing import TypeVar, Generic
from struct import Struct
import patricia

T = TypeVar('T', bound=StandardObject)

class Node(InlineObject, Generic[T]):
    struct = Struct('ihhii')
    refbit: int
    left_index: int
    right_index: int
    name: str
    content: T
    def __init__(self, name: str, content: T) -> None:
        super().__init__()
        self.name = name
        self.content = content
        self.refbit = -1
        self.left_index = 0
        self.right_index = 0

    def values(self) -> tuple:
        return (self.refbit, self.left_index, self.right_index, self.name, self.content)

class DICT(StandardObject, Generic[T]):
    signature = Signature('DICT')
    section_size = 0
    nodes: list[Node]
    def __init__(self) -> None:
        super().__init__()
        self.nodes = [Node('', None)]

    def refresh_struct(self):
        self.struct = Struct('4sii' + Node.struct.format * len(self.nodes))

    def values(self) -> tuple:
        return (self.signature, self.section_size, self.len()) + tuple(self.nodes)

    def len(self):
        return len(self.nodes) - 1
    
    def add(self, name: str, data: T):
        self.nodes.append(Node(name, data))
        self.regenerate()

    def regenerate(self):
        self.nodes[1:] = sorted(self.nodes[1:], key=lambda n: (-len(n.name), n.name))
        tree = patricia.generate([n.name for n in self.nodes if n != self.nodes[0]])
        tree.root.idx_entry = -1
        for n in self.nodes:
            p = tree.get(n.name)
            if n != self.nodes[0]: n.refbit = p.refbit
            n.left_index = p.left.idx_entry + 1
            n.right_index = p.right.idx_entry + 1
    
class DictInfo(InlineObject, Generic[T]):
    struct = Struct('ii')
    dict: DICT
    def __init__(self) -> None:
        super().__init__()
        self.dict = DICT()
    def values(self) -> tuple:
        return (self.dict.len(), self.dict if self.dict.len() else None)