import pytest


class TestString:
    def test_isdecimal(self):
        string = '824'
        assert string.isdecimal()

    @pytest.mark.parametrize('string', ['string', '\nstring', 'string\n', '\nstring\n', ' string '])
    def test_strip(self, string):
        assert string.strip() == 'string'

    def test_lower(self):
        string = 'StrING'
        assert string.lower() == 'string'

    def test_concat(self):
        str1 = 'first'
        str2 = 'second'
        assert str1 + str2 == 'firstsecond'

    def test_mult(self):
        string = 'word'
        assert string * 3 == 'wordwordword'
