from sequence_type import SequenceType


def test_sequence_type():
    assert SequenceType.morning_routine.name == 'morning_routine'
    assert SequenceType.evening_relaxation.value == 'evening_relaxation'
    assert SequenceType.quick_energy_boost.name == 'quick_energy_boost'
    assert SequenceType.deep_stretch.value == 'deep_stretch'
    assert SequenceType.strength_building.name == 'strength_building'
