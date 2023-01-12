import pytest


def is_triangle(a, b, c):
    if a > b:
        if a > c:
            return a < b + c
        else:
            return c < a + b
    else:
        if b > c:
            return b < a + c
        else:
            return c < a + b


@pytest.mark.parametrize("a", [-1, 0, 1, 3], ids=['neg', 'nul', 'not value', 'good'])
@pytest.mark.parametrize("b", [-4, 0, 4, 4], ids=['neg', 'nul', 'not value', 'good'])
@pytest.mark.parametrize("c", [-5, 0, 5, 5], ids=['neg', 'nul', 'not value', 'good'])
def test_triaangle_check(a, b, c):
    result = is_triangle(a, b, c)
    print("a: {}, b: {}, c: {}, Треугольник: {}".format(a, b, c, result))
    assert result is True
