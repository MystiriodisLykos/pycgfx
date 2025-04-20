from abc import ABC, abstractmethod
import struct
from collections import OrderedDict
from typing import Generic, TypeVar

T = TypeVar('T')

class Signature:
    data: str
    def __init__(self, data) -> None:
        self.data = data

class StringTable:
    table: OrderedDict[bytes, int]
    total = 0
    padding: int
    offset: int

    def __init__(self) -> None:
        self.table = OrderedDict()

    @staticmethod
    def correct(s: bytes | str) -> bytes:
        if isinstance(s, str):
            return s.encode() + b'\0'
        elif len(s) % 128 != 0:
            return s + b'\0' * (128 - len(s) % 128)
        return s

    def add(self, s: bytes | str):
        s = self.correct(s)
        if s not in self.table:
            self.table[s] = self.total
            self.total += len(s)

    def prepare(self, offset: int) -> int:
        self.offset = offset
        self.padding = 4 - (self.total % 4)
        self.total += self.padding
        return offset + self.total
    
    def size(self) -> int:
        return self.total
    
    def empty(self) -> bool:
        return len(self.table) == 0
    
    def get(self, s: str) -> int:
        return self.offset + self.table[self.correct(s)]
    
    def write(self) -> bytes:
        return b''.join(self.table.keys()) + b'\0' * self.padding


class BaseObject(ABC):
    struct: struct.Struct
    offset: int
    inline = False

    def refresh_struct(self):
        pass

    @abstractmethod
    def values(self) -> tuple:
        pass

    def flat_values(self):
        self.refresh_struct()
        for v in self.values():
            if isinstance(v, InlineObject):
                yield from v.flat_values()
            else:
                yield v

    def real_values(self, strings, imag) -> tuple:
        values = []
        fmt_pos = 0
        offset = self.offset
        for v in self.flat_values():
            # add values
            if isinstance(v, StandardObject):
                values.append(v.offset - offset)
            elif isinstance(v, InlineObject):
                values += list(v.real_values(strings, imag))
            elif isinstance(v, Reference):
                values.append(v.obj.offset - offset)
            elif isinstance(v, Signature):
                values.append(v.data.encode())
            elif isinstance(v, str):
                # string (0 if empty)
                values.append(strings.get(v) - offset if v else 0)
            elif isinstance(v, bytes):
                # data
                values.append(len(v))
                values.append(imag.get(v) - offset if v else 0)
            elif v is None:
                # null
                values.append(0)
            else:
                values.append(v)
            # update offset
            if isinstance(v, InlineObject):
                fmt_pos += v.size()
            else:
                fmt_pos += 1
                while fmt_pos < len(self.struct.format):
                    if self.struct.format[fmt_pos] == 'x':
                        fmt_pos += 1
                        continue
                    try:
                        offset = self.offset + struct.calcsize(self.struct.format[:fmt_pos])
                        break
                    except struct.error:
                        if self.struct.format[fmt_pos-1:fmt_pos+1] != '4s':
                            raise RuntimeError(f"can't use numbers other than 4s (found {self.struct.format[fmt_pos:fmt_pos+2]})")
                        fmt_pos += 1
                        continue
        return values

    def prepare(self, offset: int, strings: StringTable, imag: StringTable) -> int:
        """offset is current offset, returns new offset"""
        self.refresh_struct()
        self.offset = offset
        values = self.values()
        old_len = 0
        while old_len != len(values):
            old_len = len(values)
            values = [vv for v in values for vv in (v.values() if isinstance(v, InlineObject) else [v])]
        offset = self.offset + self.size()
        for v in values:
            if isinstance(v, StandardObject):
                offset = v.prepare(offset, strings, imag)
            elif isinstance(v, str):
                # string (not signature)
                strings.add(v)
            elif isinstance(v, bytes):
                imag.add(v)
        return offset

    def write(self, strings: StringTable, imag: StringTable) -> bytes:
        values = self.real_values(strings, imag)
        data = self.struct.pack(*values)
        for v in self.flat_values():
            if isinstance(v, StandardObject):
                data += v.write(strings, imag)
        return data

    def size(self) -> int:
        self.refresh_struct()
        return self.struct.size

class StandardObject(BaseObject):
    pass

class InlineObject(BaseObject):
    pass


class Reference:
    def __init__(self, obj: StandardObject):
        self.obj = obj

class ListData(StandardObject, Generic[T]):
    contents: list[T]
    def __init__(self, list = None) -> None:
        super().__init__()
        self.contents = list if list else []
    def refresh_struct(self):
        self.struct = struct.Struct('i' * len(self.contents))
    def values(self) -> tuple:
        return tuple(self.contents)
    def len(self):
        return len(self.contents)
    
class List(InlineObject, Generic[T]):
    data: ListData
    def __init__(self, list = None) -> None:
        super().__init__()
        self.data = ListData(list)
    def values(self) -> tuple:
        return (self.data.len(), self.data if self.data.len() else None)

class Vector3(InlineObject):
    struct = struct.Struct('fff')
    x: float
    y: float
    z: float
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def values(self) -> tuple:
        return (self.x, self.y, self.z)

class Matrix(InlineObject):
    struct = struct.Struct('f'*12)
    columns: list[Vector3]
    def __init__(self, col1, col2, col3, col4):
        self.columns = [col1, col2, col3, col4]
    def values(self) -> tuple:
        return tuple(self.columns)

class OrientationMatrix(InlineObject):
    struct = struct.Struct('f'*9)
    columns: list[Vector3]
    def __init__(self, col1, col2, col3):
        self.columns = [col1, col2, col3]
    def values(self) -> tuple:
        return tuple(self.columns)