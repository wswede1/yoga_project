from model.pose_sequence import PoseSequence
from model.yoga_pose import YogaPose
from model.enums import SequenceType


def test_pose_sequence_initialization():
    pose1 = YogaPose(
        english_name="Downward-Facing Dog",
        sanskrit_name="Adho Mukha Svanasana",
        pose_type="Inversion, Strength",
        target_body_parts="Hamstrings, Shoulders",
        instructions="Press through the palms and lift your hips to form an inverted V.",
    )
    pose2 = YogaPose(
        english_name="Mountain Pose",
        sanskrit_name="Tadasana",
        pose_type="Standing, Foundation",
        target_body_parts="Full Body",
        instructions="Stand tall, root down through your feet, and lengthen the crown of your head.",
    )

    sequence = PoseSequence(
        name="Morning Routine",
        poses=[pose1, pose2],
        sequence_type=SequenceType.morning_routine,
    )

    assert sequence.name == "Morning Routine"
    assert sequence.poses == [pose1, pose2]
    assert sequence.sequence_type == SequenceType.morning_routine
