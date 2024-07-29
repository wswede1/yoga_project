from model.enums import BodyPart, PoseCategory, YogaStyle, PoseBenefit, SequenceType


def test_body_part_values():
    assert BodyPart.hips.value == "hips"
    assert BodyPart.shoulders.value == "shoulders"
    assert BodyPart.lower_back.value == "lower_back"
    assert BodyPart.upper_back.value == "upper_back"
    assert BodyPart.neck.value == "neck"
    assert BodyPart.knees.value == "knees"
    assert BodyPart.wrists.value == "wrists"


def test_pose_benefit():
    assert PoseBenefit.stress_relief.name == 'stress_relief'
    assert PoseBenefit.back_pain_relief.value == 'back_pain_relief'
    assert PoseBenefit.hip_opening.name == 'hip_opening'
    assert PoseBenefit.shoulder_strength.value == 'shoulder_strength'
    assert PoseBenefit.core_strength.name == 'core_strength'


def test_pose_category():
    assert PoseCategory.restorative.name == 'restorative'
    assert PoseCategory.strength.value == 'strength'
    assert PoseCategory.flexibility.name == 'flexibility'
    assert PoseCategory.balance.value == 'balance'
    assert PoseCategory.meditation.name == 'meditation'


def test_sequence_type():
    assert SequenceType.morning_routine.name == 'morning_routine'
    assert SequenceType.evening_relaxation.value == 'evening_relaxation'
    assert SequenceType.quick_energy_boost.name == 'quick_energy_boost'
    assert SequenceType.deep_stretch.value == 'deep_stretch'
    assert SequenceType.strength_building.name == 'strength_building'


def test_yoga_style():
    assert YogaStyle.Hatha.name == 'Hatha'
    assert YogaStyle.Vinyasa.value == 'Vinyasa'
    assert YogaStyle.Ashtanga.name == 'Ashtanga'
