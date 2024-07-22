from yoga_pose import YogaPose
from body_part import BodyPart
from pose_category import PoseCategory
from yoga_style import YogaStyle
from pose_benefit import PoseBenefit


def test_yoga_pose_initialization():
    pose = YogaPose(
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
    assert pose.category == PoseCategory.flexibility
    assert pose.style == YogaStyle.Hatha
    assert PoseBenefit.stress_relief in pose.benefits
