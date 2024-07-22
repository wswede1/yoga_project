from typing import List
from yoga_pose import YogaPose
from sequence_type import SequenceType

class PoseSequence:
    def __init__(self, sequence: List[YogaPose], sequence_type: SequenceType):
        self.sequence = sequence
        self.sequence_type = sequence_type
