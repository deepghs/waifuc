import pytest

from waifuc.utils import IDOrder


@pytest.fixture()
def idorder():
    yield IDOrder()


@pytest.mark.unittest
class TestUtilsIdorder:
    @pytest.mark.parametrize(['try_cnt'], [(i_,) for i_ in range(1, 11)])
    def test_idorder(self, idorder, try_cnt):
        assert not idorder.is_set_id(0)
        assert not idorder.is_set_id(1)
        assert not idorder.is_set_id(2)
        assert not idorder.is_set_id(10)

        assert not idorder.wait_for_id(0, timeout=0.5)
        assert not idorder.wait_for_id(2, timeout=0.5)
        idorder.set_id(0)
        assert idorder.wait_for_id(0)
        assert not idorder.wait_for_id(2, timeout=0.5)

        assert not idorder.wait_for_id(2, timeout=0.5)
        idorder.set_id(2)
        assert idorder.wait_for_id(2)
        assert idorder.is_set_id(2)
        assert idorder.wait_for_id(0)
        assert idorder.is_set_id(0)
        assert not idorder.is_set_id(1)
        assert idorder.is_set_id(2)
        assert not idorder.is_set_id(10)
