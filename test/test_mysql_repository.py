from unittest.mock import MagicMock

from db.mysql_repository import MySQLRepository
from model.yoga_pose import YogaPose


def setup_repo(monkeypatch, fetch_result=None, fetchone_result=None):
    repo = MySQLRepository()
    fake_cursor = MagicMock()
    fake_connection = MagicMock()

    fake_cursor.fetchall.return_value = fetch_result or []
    fake_cursor.fetchone.return_value = fetchone_result
    fake_cursor.lastrowid = 7

    fake_connection.cursor.return_value = fake_cursor

    monkeypatch.setattr(repo, "_get_connection", lambda: fake_connection)

    return repo, fake_connection, fake_cursor


def test_get_poses_by_body_part_returns_models(monkeypatch):
    fetch_result = [
        {
            "english_name": "Thread the Needle",
            "sanskrit_name": "Parsva Balasana",
            "pose_type": "Twist, Restorative",
            "target_body_parts": "Shoulders, Upper Back",
            "instructions": "Slide your arm underneath and rest on the side body.",
        }
    ]
    repo, connection, cursor = setup_repo(monkeypatch, fetch_result=fetch_result)

    poses = repo.get_poses_by_body_part("shoulders")

    assert len(poses) == 1
    assert isinstance(poses[0], YogaPose)
    assert poses[0].english_name == "Thread the Needle"
    assert cursor.execute.call_args[0][1] == ("%shoulders%",)
    connection.cursor.assert_called_with(dictionary=True)
    cursor.close.assert_called_once()
    connection.close.assert_called_once()


def test_add_pose_commits_and_returns_id(monkeypatch):
    repo, connection, cursor = setup_repo(monkeypatch)
    pose = YogaPose(
        english_name="Sample Pose",
        sanskrit_name="Samplerasana",
        pose_type="Balance",
        target_body_parts="Core",
        instructions="Stay centered and breathe.",
    )

    new_id = repo.add_pose(pose)

    assert new_id == cursor.lastrowid
    connection.commit.assert_called_once()
    cursor.execute.assert_called_once()
    cursor.close.assert_called_once()
    connection.close.assert_called_once()


def test_load_pose_returns_yoga_pose(monkeypatch):
    row = {
        "english_name": "Cat-Cow Stretch",
        "sanskrit_name": "Marjaryasana-Bitilasana",
        "pose_type": "Warm-Up",
        "target_body_parts": "Spine, Neck",
        "instructions": "Alternate between rounding and arching the spine.",
    }
    repo, connection, cursor = setup_repo(monkeypatch, fetchone_result=row)

    pose = repo.load_pose("Cat-Cow Stretch")

    assert pose.english_name == "Cat-Cow Stretch"
    cursor.execute.assert_called_once()
    cursor.close.assert_called_once()
    connection.close.assert_called_once()


def test_load_pose_returns_none_when_missing(monkeypatch):
    repo, connection, cursor = setup_repo(monkeypatch, fetchone_result=None)

    pose = repo.load_pose("Unknown")

    assert pose is None
    cursor.close.assert_called_once()
    connection.close.assert_called_once()
