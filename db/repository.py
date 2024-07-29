import abc
from model.yoga_pose import YogaPose


class Repository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def add_pose(self, pose: YogaPose):
        """Add a new yoga pose to the database."""

    @abc.abstractmethod
    def load_pose(self, name: str) -> YogaPose:
        """Load a yoga pose from the database by its name."""

#     @abc.abstractmethod
#     def add_sequence(self, sequence: PoseSequence):
#         """Add a new pose sequence to the database."""
#
#     @abc.abstractmethod
#     def load_sequence(self, sequence_type: str) -> PoseSequence:
#         """Load a pose sequence from the database by its type."""
