from model.yoga_service import YogaService
from model.yoga_pose import YogaPose


class StubRepository:
    def __init__(self):
        self.added_poses = []
        self.pose_lookup = {}
        self.pose_by_target = {}

    def add_pose(self, pose):
        self.added_poses.append(pose)
        return pose

    def load_pose(self, name):
        return self.pose_lookup.get(name)

    def get_poses_by_body_part(self, body_part):
        return self.pose_by_target.get(body_part, [])


def build_pose(name):
    return YogaPose(
        english_name=name,
        sanskrit_name="Testasana",
        pose_type="Balance, Strength",
        target_body_parts="Hips, Core",
        instructions="Hold steady for five breaths.",
    )


def test_add_pose():
    repository = StubRepository()
    service = YogaService(repository)

    pose = build_pose("Test Pose")
    result = service.add_pose(pose)

    assert result.english_name == "Test Pose"
    assert repository.added_poses == [pose]


def test_get_pose():
    repository = StubRepository()
    service = YogaService(repository)
    pose = build_pose("Rest Pose")
    repository.pose_lookup["Rest Pose"] = pose

    result = service.get_pose("Rest Pose")

    assert result is pose


def test_get_poses_by_body_part():
    repository = StubRepository()
    service = YogaService(repository)
    pose = build_pose("Core Twist")
    repository.pose_by_target["hips"] = [pose]

    result = service.get_poses_by_body_part("hips")

    assert result == [pose.to_dict()]
