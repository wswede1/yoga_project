from typing import List
from body_part import BodyPart
from pose_category import PoseCategory
from yoga_style import YogaStyle
from pose_benefit import PoseBenefit


class YogaPose:
    def __init__(self, name: str, instructions: str, target_body_parts: List[BodyPart], category: PoseCategory,
                 style: YogaStyle, benefits: List[PoseBenefit]):
        self.name = name
        self.instructions = instructions
        self.target_body_parts = target_body_parts
        self.category = category
        self.style = style
        self.benefits = benefits

    @property
    def get_instructions(self):
        return self.instructions
