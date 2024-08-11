from typing import List


class YogaPose:
    """Class representing a yoga pose"""

    def __init__(self, english_name: str, sanskrit_name: str, pose_type: str,
                 target_body_parts: str, instructions: str):
        self.english_name = english_name
        self.sanskrit_name = sanskrit_name
        self.pose_type = pose_type
        self.target_body_parts = target_body_parts
        self.instructions = instructions

    @property
    def get_instructions(self):
        return self.instructions
