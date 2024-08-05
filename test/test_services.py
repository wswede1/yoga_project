from model.yoga_service import YogaService
from db.mysql_repository import MySQLRepository
from model.yoga_pose import YogaPose
from model.enums import BodyPart

# Initialize the service repo
repository = MySQLRepository()
service = YogaService(repository)


def test_add_pose():
    pose = YogaPose(name="Test Pose", instructions="Test instructions")
    repository.add_pose = lambda pose: pose  # Mock method
    result = service.add_pose(pose)
    assert result.name == "Test Pose"
    assert result.instructions == "Test instructions"


def test_get_pose():
    pose = YogaPose(name="Test Pose", instructions="Test instructions")
    repository.load_pose = lambda name: pose  # Mock method
    result = service.get_pose("Test Pose")
    assert result.name == "Test Pose"
    assert result.instructions == "Test instructions"


def test_get_poses_by_body_part():
    pose = YogaPose(name="Test Pose", instructions="Test instructions")
    repository.get_poses_by_body_part = lambda body_part: [pose]  # Mock method
    result = service.get_poses_by_body_part("hips")
    assert len(result) == 1
    assert result[0].name == "Test Pose"
    assert result[0].instructions == "Test instructions"


if __name__ == "__main__":
    test_add_pose()
    test_get_pose()
    test_get_poses_by_body_part()
    print("All tests passed!")
