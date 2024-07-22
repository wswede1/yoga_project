from pose_category import PoseCategory


def test_pose_category():
    assert PoseCategory.restorative.name == 'restorative'
    assert PoseCategory.strength.value == 'strength'
    assert PoseCategory.flexibility.name == 'flexibility'
    assert PoseCategory.balance.value == 'balance'
    assert PoseCategory.meditation.name == 'meditation'
