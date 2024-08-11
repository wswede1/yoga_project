import abc
from typing import List
from model.yoga_pose import YogaPose


class Repository(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_poses_by_body_part(self, body_part: str) -> List[YogaPose]:
        raise NotImplementedError

    @abc.abstractmethod
    def add_pose(self, pose: YogaPose) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def load_pose(self, name: str) -> YogaPose:
        raise NotImplementedError
