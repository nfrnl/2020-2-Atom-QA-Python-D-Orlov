import random

import pytest


@pytest.fixture
def make_randomised_set():
    def _make_randomised_set():
        return set(random.sample(range(1000000), random.randint(1, 10)))

    return _make_randomised_set


class TestSet:
    def test_intersection(self):
        set1 = {3, 6, 1, 2, 9, 12, 5}
        set2 = {12, 5, 4, 1, 90, 23}
        assert set1.intersection(set2) == {1, 5, 12}

    def test_union(self):
        set1 = {3, 6, 1, 2, 9, 12, 5}
        set2 = {12, 5, 4, 1, 90, 23}
        assert set1.union(set2) == {1, 2, 3, 4, 5, 6, 9, 12, 23, 90}

    def test_clear(self, make_randomised_set):
        set1 = make_randomised_set()
        set1.clear()
        assert len(set1) == 0

    @pytest.mark.parametrize('set1, result', [({1, 4, 7}, False), ({4, 7}, True)])
    def test_issubset(self, set1, result):
        set2 = {2, 4, 7}
        assert set1.issubset(set2) == result

    def test_remove(self):
        set1 = {1, 2, 6, 9}
        set1.remove(6)
        assert set1 == {1, 2, 9}
