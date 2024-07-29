from model.yoga_pose import YogaPose
from model.enums import SequenceType
from model.pose_sequence import PoseSequence


def test_pose_sequence_initialization():
    pose1 = YogaPose(
        id=1,
        name="Downward Dog",
        instructions="Start on all fours...",
        target_body_parts=[],
        category=None,  # Placeholder value
        style=None,  # Placeholder value
        benefits=[]
    )
    pose2 = YogaPose(
        id=2,
        name="Mountain Pose",
        instructions="Stand tall with feet together...",
        target_body_parts=[],
        category=None,  # Placeholder value
        style=None,  # Placeholder value
        benefits=[]
    )
    sequence = PoseSequence(name="Morning Routine", poses=[pose1, pose2], sequence_type=SequenceType.morning_routine)
    assert sequence.name == "Morning Routine"
    assert sequence.poses == [pose1, pose2]
    assert sequence.sequence_type == SequenceType.morning_routine
