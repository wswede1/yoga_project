from typing import List
from model.yoga_pose import YogaPose
from model.enums import SequenceType


class PoseSequence:
    def __init__(self, name: str, poses: List[YogaPose], sequence_type: SequenceType):
        self.name = name
        self.poses = poses
        self.sequence_type = sequence_type
