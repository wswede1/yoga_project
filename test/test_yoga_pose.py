from model.yoga_pose import YogaPose


def test_yoga_pose_to_dict_splits_lists():
    pose = YogaPose(
        english_name="Downward-Facing Dog",
        sanskrit_name="Adho Mukha Svanasana",
        pose_type="Inversion, Strength",
        target_body_parts="Hamstrings, Shoulders",
        instructions="Press through the palms and lift your hips to form an inverted V.",
    )

    data = pose.to_dict()

    assert data["english_name"] == "Downward-Facing Dog"
    assert data["sanskrit_name"] == "Adho Mukha Svanasana"
    assert data["pose_type"] == ["Inversion", "Strength"]
    assert data["target_body_parts"] == ["Hamstrings", "Shoulders"]
    assert "press through the palms" in data["instructions"].lower()
