# straight translation from https://github.com/Gericom/EveryFileExplorer/blob/master/3DS/NintendoWare/GFX/PatriciaTreeGenerator.cs

class Node:
    refbit: int
    left: 'Node'
    right: 'Node'
    idx_entry: int
    name: str

def get_bit(name: str, bit: int) -> bool:
    return ((ord(name[bit // 8]) >> (bit & 7)) & 1) != 0

class PatTree:
    root: Node
    string_length: int

    def __init__(self, maxlen) -> None:
        self.string_length = maxlen
        root = Node()
        root.refbit = maxlen * 8 - 1
        root.left = root
        root.right = root
        root.idx_entry = 0
        root.name = '\0' * maxlen
        self.root = root

    def add(self, name: str, index: int):
        name = name.ljust(self.string_length, '\0')
        new_node = Node()
        new_node.name = name
        new_node.idx_entry = index
        current = self.root
        left = current.left
        while current.refbit > left.refbit:
            current = left
            left = current.right if get_bit(name, current.refbit) else current.left

        bit = self.string_length * 8 - 1
        while get_bit(left.name, bit) == get_bit(name, bit):
            bit -= 1

        current = self.root
        left = current.left
        while current.refbit > left.refbit and left.refbit > bit:
            current = left
            left = current.right if get_bit(name, current.refbit) else current.left
        
        new_node.refbit = bit
        new_node.left = left if get_bit(name, bit) else new_node
        new_node.right = new_node if get_bit(name, bit) else left
        if get_bit(name, current.refbit):
            current.right = new_node
        else:
            current.left = new_node
        return new_node
    
    def get(self, name: str) -> Node:
        name = name.ljust(self.string_length, '\0')
        current = self.root
        while current.name != name and current.refbit > current.left.refbit:
            current = current.right if get_bit(name, current.refbit) else current.left
        return current

def generate(names: list[str]) -> PatTree:
    tree = PatTree(max(len(n) for n in names))
    for i,n in enumerate(names):
        tree.add(n, i)
    return tree