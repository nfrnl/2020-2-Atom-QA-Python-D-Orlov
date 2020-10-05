import pytest


@pytest.fixture
def ready_dict():
    return {'name': 'Jake', 'age': 19, 'city': 'London'}


class TestDict:
    def test_clear(self, ready_dict):
        d = ready_dict
        d.clear()
        assert len(d) == 0

    def test_pop(self, ready_dict):
        d = ready_dict
        d.pop('name')
        assert d == {'age': 19, 'city': 'London'}

    def test_brackets(self, ready_dict):
        d = ready_dict
        assert d['age'] == 19

    def test_brackets_raises_exc(self, ready_dict):
        d = ready_dict
        with pytest.raises(KeyError):
            d['education']

    @pytest.mark.parametrize('default', [0, 1, 'no_data'])
    def test_setdefault(self, ready_dict, default):
        d = ready_dict
        assert d.setdefault('education', default) == default
