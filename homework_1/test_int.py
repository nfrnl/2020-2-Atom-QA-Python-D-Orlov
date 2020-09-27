import pytest


class TestInt:
    def test_sum(self):
        assert 4 + 192 == 196

    def test_sub(self):
        assert 22 - 82 == -60

    def test_mult(self):
        assert 3 * 4 == 12

    def test_pow(self):
        assert 4 ** 3 == 64

    @pytest.mark.parametrize('divisor, expected', [(2, 0), (3, 1), (5, 4)])
    def test_mod(self, divisor, expected):
        assert 4 % divisor == expected
