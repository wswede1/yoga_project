from body_part import BodyPart

def test_body_part_values():
    assert BodyPart.hips.value == "hips"
    assert BodyPart.shoulders.value == "shoulders"
    assert BodyPart.lower_back.value == "lower_back"
    assert BodyPart.upper_back.value == "upper_back"
    assert BodyPart.neck.value == "neck"
    assert BodyPart.knees.value == "knees"
    assert BodyPart.wrists.value == "wrists"
