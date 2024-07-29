from enum import Enum


class BodyPart(Enum):
    hips = "hips"
    shoulders = "shoulders"
    lower_back = "lower_back"
    upper_back = "upper_back"
    neck = "neck"
    knees = "knees"
    wrists = "wrists"


class PoseCategory(Enum):
    restorative = "restorative"
    strength = "strength"
    flexibility = "flexibility"
    balance = "balance"
    meditation = "meditation"


class YogaStyle(Enum):
    Hatha = "Hatha"
    Vinyasa = "Vinyasa"
    Ashtanga = "Ashtanga"


class PoseBenefit(Enum):
    stress_relief = "stress_relief"
    back_pain_relief = "back_pain_relief"
    hip_opening = "hip_opening"
    shoulder_strength = "shoulder_strength"
    core_strength = "core_strength"


class SequenceType(Enum):
    morning_routine = "morning_routine"
    evening_relaxation = "evening_relaxation"
    quick_energy_boost = "quick_energy_boost"
    deep_stretch = "deep_stretch"
    strength_building = "strength_building"
