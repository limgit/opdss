import jinja2
from enum import Enum, auto


class Signage:
    pass


class Scene:
    pass


class Frame:
    pass


class Schedule:
    pass


class Transition:
    pass


class ScheduleType(Enum):
    ALWAYS_VISIBLE = auto()
    ALWAYS_HIDDEN = auto()
    VISIBLE_ON_TIME = auto()
    HIDDEN_ON_TIME = auto()


class TransitionTypeEnum(Enum):
    NONE = auto()
    PUSH = auto()
    FADE = auto()
