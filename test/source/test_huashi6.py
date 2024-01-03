import pytest

from waifuc.source import Huashi6Source


@pytest.mark.ignore
class TestSourceHuashi6:

    def test_huashi6(self, huashi6_nian):
        source = Huashi6Source('明日方舟 年')
        items = list(source[:10])
        assert len(items) == 10
