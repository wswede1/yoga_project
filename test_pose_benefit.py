from pose_benefit import PoseBenefit


def test_pose_benefit():
    assert PoseBenefit.stress_relief.name == 'stress_relief'
    assert PoseBenefit.back_pain_relief.value == 'back_pain_relief'
    assert PoseBenefit.hip_opening.name == 'hip_opening'
    assert PoseBenefit.shoulder_strength.value == 'shoulder_strength'
    assert PoseBenefit.core_strength.name == 'core_strength'
