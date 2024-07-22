from pose_sequence import PoseSequence
from yoga_pose import YogaPose
from sequence_type import SequenceType


def test_pose_sequence_initialization():
    pose1 = YogaPose("Downward Dog", "Start on all fours...", [], None, None, [])
    pose2 = YogaPose("Warrior II", "Stand with legs wide apart...", [], None, None, [])
    sequence = PoseSequence(
        sequence=[pose1, pose2],
        sequence_type=SequenceType.morning_routine
    )

    assert sequence.sequence_type == SequenceType.morning_routine
    assert pose1 in sequence.sequence
