from enum import StrEnum, auto


class BiologicalGender(StrEnum):
    MALE = auto()
    FEMALE = auto()


class WeightTarget(StrEnum):
    LOSE = auto()
    MAINTAIN = auto()
    GAIN = auto()
