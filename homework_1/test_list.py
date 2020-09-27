import random

import pytest


@pytest.fixture
def make_randomised_list():
    def _make_randomised_list():
        return random.sample(range(1000000), random.randint(1, 10))

    return _make_randomised_list


class TestList:
    @pytest.mark.parametrize('elem', [0, 1, 'word', 0.22, (0, 1)])
    def test_append(self, elem, make_randomised_list):
        lst = make_randomised_list()
        lst.append(elem)
        assert lst[len(lst) - 1] == elem

    def test_pop(self, make_randomised_list):
        lst = make_randomised_list()
        last_elem_value = lst[len(lst) - 1]
        assert lst.pop() == last_elem_value

    def test_pop_empty(self):
        lst = []
        with pytest.raises(IndexError):
            lst.pop()

    def test_clear(self, make_randomised_list):
        lst = make_randomised_list()
        lst.clear()
        assert len(lst) == 0

    def test_concat(self, make_randomised_list):
        lst1 = make_randomised_list()
        lst2 = make_randomised_list()
        lst3 = lst1 + lst2
        assert lst3 == [*lst1, *lst2]
