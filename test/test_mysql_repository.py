from db.mysql_repository import MySQLRepository
from model.yoga_pose import YogaPose

repo = MySQLRepository()

def test_add_pose():
    test_pose = YogaPose(
        id=None,
        name='Test Pose',
        instructions='Test instructions',
        target_body_parts=[],
        category=None,
        style=None,
        benefits=[]
    )
    repo.add_pose(test_pose)
    added_pose = repo.load_pose('Test Pose')
    assert added_pose is not None
    assert added_pose.name == 'Test Pose'
    assert added_pose.instructions == 'Test instructions'

def test_load_pose():
    loaded_pose = repo.load_pose(name="Test Pose")
    assert loaded_pose is not None
    assert loaded_pose.name == "Test Pose"
    assert loaded_pose.instructions == "Test instructions"

