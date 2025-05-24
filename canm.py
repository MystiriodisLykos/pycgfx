from shared import ColorFloat, InlineObject, StandardObject, Signature, Vector3, Vector4
from dict import DictInfo
from enum import IntEnum, IntFlag

class Vector2Flag(IntFlag):
    XConst = 1
    YConst = 2
    XIgnore = 4
    YIgnore = 8

class TransformQuaternionFlag(IntFlag):
    TranslationIgnore = 8
    RotationIgnore = 16
    ScaleIgnore = 32

class RgbaColorFlags(IntFlag):
    IgnoreRed = 16
    IgnoreGreen = 32
    IgnoreBlue = 64
    IgnoreAlpha = 128

class PrimitiveType(IntEnum):
    Float = 0
    Int = 1
    Boolean = 2
    Vector2 = 3
    Vector3 = 4
    Transform = 5
    RgbaColor = 6
    Texture = 7
    TransformQuaternion = 8
    TransformMatrix = 9

class AnimationCurve(StandardObject):
    start_frame = 0
    end_frame = 600
    pre_repeat_method = 0
    post_repeat_method = 0
    flags = 0
    def values(self) -> tuple:
        return (self.start_frame, self.end_frame,
                self.pre_repeat_method | (self.post_repeat_method << 8),
                self.flags)

class FloatSegment(StandardObject):
    start_frame = 0
    end_frame = 0
    flags = 0

class FloatAnimationCurve(AnimationCurve):
    segments: list[FloatSegment]
    def __init__(self) -> None:
        self.segments = []
    def values(self) -> tuple:
        return super().values() + (len(self.segments), *self.segments)

class Vector3AndFlags(InlineObject):
    value: Vector3
    flags = 0
    def __init__(self) -> None:
        self.value = Vector3()
    def values(self) -> tuple:
        return (self.value, self.flags)

class Vector3AnimationCurve(AnimationCurve):
    frames: list[Vector3AndFlags]
    def __init__(self) -> None:
        self.frames = []
    def values(self) -> tuple:
        if (self.flags[0] & 1) == 0:
            assert len(self.frames) == self.end_frame - self.start_frame
        return super().values() + (
            (self.frames[0],) if self.flags[0] & 1 else tuple(self.frames)
        )

class QuaternionAndFlags(InlineObject):
    value: Vector4
    flags = 0
    def __init__(self) -> None:
        self.value = Vector4()
    def values(self) -> tuple:
        return (self.value, self.flags)

class QuaternionAnimationCurve(AnimationCurve):
    frames: list[QuaternionAndFlags]
    def __init__(self) -> None:
        self.frames = []
    def values(self) -> tuple:
        if (self.flags[0] & 1) == 0:
            assert len(self.frames) == self.end_frame - self.start_frame
        return super.values() + (
            (self.frames[0],) if self.flags[0] & 1 else tuple(self.frames)
        )

class ColorSegment(StandardObject):
    float_segment: FloatSegment
    unknown = 0.0
    data: list[ColorFloat]
    def __init__(self) -> None:
        self.float_segment = FloatSegment()
        self.data = []
    def values(self) -> tuple:
        return (self.float_segment, len(self.data), self.unknown, *self.data)

class ColorAnimationCurve(AnimationCurve):
    segments: list[ColorSegment]
    def __init__(self) -> None:
        self.segments = []
    def values(self) -> tuple:
        return super().values() + (len(self.segments), *self.segments)

class CANMBone(StandardObject):
    flags = 0
    bone_path = ''
    unknown1 = ''
    unknown2 = ''
    primitive_type = 0
    def values(self):
        return (self.flags, self.bone_path, self.unknown1, self.unknown2, self.primitive_type)

class CANMBoneVector2(CANMBone):
    flags = Vector2Flag(0)
    primitive_type = PrimitiveType.Vector2
    x_const = 0
    y_const = 0
    x_curve: FloatAnimationCurve
    y_curve: FloatAnimationCurve
    def __init__(self):
        self.x_curve = FloatAnimationCurve()
        self.y_curve = FloatAnimationCurve()
    def values(self):
        return super().values() + (
            self.x_const if Vector2Flag.XConst in self.flags else (None if Vector2Flag.XIgnore in self.flags else self.x_curve),
            self.y_const if Vector2Flag.YConst in self.flags else (None if Vector2Flag.YIgnore in self.flags else self.y_curve))

class CANMBoneTransformQuaternion(CANMBone):
    flags = TransformQuaternionFlag(0)
    rotation: QuaternionAnimationCurve
    translation: Vector3AnimationCurve
    scale: Vector3AnimationCurve
    def __init__(self):
        self.rotation = QuaternionAnimationCurve()
        self.translation = Vector3AnimationCurve()
        self.scale = Vector3AnimationCurve()
    def values(self):
        return super().values() + (
            None if TransformQuaternionFlag.RotationIgnore in self.flags else self.rotation,
            None if TransformQuaternionFlag.TranslationIgnore in self.flags else self.translation,
            None if TransformQuaternionFlag.ScaleIgnore in self.flags else self.scale)

class CANMBoneRgbaColor(CANMBone):
    flags = RgbaColorFlags(0)
    red: ColorAnimationCurve
    green: ColorAnimationCurve
    blue: ColorAnimationCurve
    alpha: ColorAnimationCurve
    def __init__(self) -> None:
        self.red = ColorAnimationCurve()
        self.green = ColorAnimationCurve()
        self.blue = ColorAnimationCurve()
        self.alpha = ColorAnimationCurve()
    def values(self):
        return super().values() + (
            None if RgbaColorFlags.IgnoreRed in self.flags else self.red,
            None if RgbaColorFlags.IgnoreGreen in self.flags else self.green,
            None if RgbaColorFlags.IgnoreBlue in self.flags else self.blue,
            None if RgbaColorFlags.IgnoreAlpha in self.flags else self.alpha,
        )

class CANM(StandardObject):
    signature = Signature('CANM')
    revision = 0x05000000
    name = ''
    target_animation_group_name = ''
    looping = True
    frame_size = 600
    member_animations_data: DictInfo[CANMBone]
    user_data: DictInfo
    def __init__(self):
        self.member_animations_data: DictInfo[CANMBone] = DictInfo()
        self.user_data = DictInfo()
    def values(self) -> tuple:
        return (self.signature, self.revision, self.name, self.target_animation_group_name,
                self.looping, self.frame_size, self.member_animations_data, self.user_data)

