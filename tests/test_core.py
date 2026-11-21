import math

import pytest

import triplanar

def _raises(fn, exc=ValueError):
    try:
        fn()
    except exc:
        return True
    return False

def _t():
    return triplanar.Triplanar(1.0)


def _check_sum():
    return abs(sum(_t().weights((0.0, 1.0, 0.0))) - 1.0) < 1e-9


def _check_y():
    return _t().weights((0.0, 1.0, 0.0))[1] > 0.99


def _check_x():
    return _t().weights((1.0, 0.0, 0.0))[0] > 0.99


def _check_z():
    return _t().weights((0.0, 0.0, 1.0))[2] > 0.99


def _check_len():
    return len(_t().weights((0.5, 0.5, 0.0))) == 3


def _check_cont():
    a = _t().weights((0.7, 0.7, 0.1))
    b = _t().weights((0.7001, 0.6999, 0.1))
    return max(abs(x - y) for x, y in zip(a, b)) < 1e-2


def _check_bad_len():
    return _raises(lambda: _t().weights((0.0, 1.0)))


def _check_zero():
    return _raises(lambda: _t().weights((0.0, 0.0, 0.0)))


def _check_bad_sharp():
    return _raises(lambda: triplanar.Triplanar(0.0))


def _check_type():
    return isinstance(_t().weights((0.1, 0.9, 0.0)), tuple)


def _check_range():
    return all(0.0 <= v <= 1.0 for v in _t().weights((0.3, 0.6, 0.1)))


def _check_det():
    return _t().weights((0.2, 0.3, 0.4)) == _t().weights((0.2, 0.3, 0.4))


def _check_sharp():
    a = triplanar.Triplanar(1.0).weights((0.6, 0.8, 0.0))
    b = triplanar.Triplanar(4.0).weights((0.6, 0.8, 0.0))
    return a != b


def _check_negative():
    return abs(sum(_t().weights((-0.5, 0.5, 0.0))) - 1.0) < 1e-9


def _check_float():
    return isinstance(_t().weights((0.3, 0.3, 0.3))[0], float)

CASES = [("sum", "_check_sum"), ("y", "_check_y"), ("x", "_check_x"), ("z", "_check_z"), ("len", "_check_len"), ("cont", "_check_cont"), ("bad_len", "_check_bad_len"), ("zero", "_check_zero"), ("bad_sharp", "_check_bad_sharp"), ("type", "_check_type"), ("range", "_check_range"), ("det", "_check_det"), ("sharp", "_check_sharp"), ("negative", "_check_negative"), ("float", "_check_float")]


@pytest.mark.parametrize("name,check", CASES, ids=[c[0] for c in CASES])
def test_spec(name, check):
    assert globals()[check]() is True
