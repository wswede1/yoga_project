from db.repository import Repository
from model.yoga_pose import YogaPose
from model.pose_sequence import PoseSequence
from model.enums import BodyPart

class YogaService:
    def __init__(self, repository: Repository):
        self.repository = repository

    def add_pose(self, pose: YogaPose) -> YogaPose:
        return self.repository.add_pose(pose)

    def get_pose(self, name: str) -> YogaPose:
        return self.repository.load_pose(name)

    def get_poses_by_body_part(self, body_part: str) -> list[YogaPose]:
        return self.repository.get_poses_by_body_part(body_part)
