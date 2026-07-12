from vasp_constant import AUTOA, RYTOEV, HSQDTM, TPI


def test_constants_positive():
    assert AUTOA > 0
    assert RYTOEV > 0
    assert HSQDTM > 0
    assert TPI > 0
