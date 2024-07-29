from typing import List
from model.enums import BodyPart, PoseCategory, YogaStyle, PoseBenefit


class YogaPose:
    def __init__(
            self,
            id: int = None,
            name: str = "",
            instructions: str = "",
            target_body_parts: List[BodyPart] = None,
            category: PoseCategory = None,
            style: YogaStyle = None,
            benefits: List[PoseBenefit] = None
    ):
        self.id = id
        self.name = name
        self.instructions = instructions
        self.target_body_parts = target_body_parts if target_body_parts is not None else []
        self.category = category
        self.style = style
        self.benefits = benefits if benefits is not None else []

    @property
    def get_instructions(self):
        return self.instructions
