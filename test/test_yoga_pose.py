from model.yoga_pose import YogaPose
from model.enums import BodyPart, PoseCategory, YogaStyle, PoseBenefit


def test_yoga_pose_initialization():
    pose = YogaPose(
        id=1,
        name="Downward Dog",
        instructions="Start on all fours...",
        target_body_parts=[BodyPart.shoulders, BodyPart.wrists],
        category=PoseCategory.flexibility,
        style=YogaStyle.Hatha,
        benefits=[PoseBenefit.stress_relief, PoseBenefit.shoulder_strength]
    )
    assert pose.name == "Downward Dog"
    assert pose.instructions == "Start on all fours..."
    assert BodyPart.shoulders in pose.target_body_parts
    assert PoseCategory.flexibility == pose.category
    assert YogaStyle.Hatha == pose.style
    assert PoseBenefit.stress_relief in pose.benefits
