from yoga_style import YogaStyle


def test_yoga_style():
    assert YogaStyle.Hatha.name == 'Hatha'
    assert YogaStyle.Vinyasa.value == 'Vinyasa'
    assert YogaStyle.Ashtanga.name == 'Ashtanga'
