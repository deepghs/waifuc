import pytest

from waifuc.source import DuitangSource


@pytest.mark.ignore
class TestSourceDuitang:

    def test_duitang(self, duitang_nian, duitang_nian_non_strict):
        source = DuitangSource('明日方舟 年')
        items = list(source[:10])

        assert len(items) == 10
        for item in items:
            assert '明日方舟' in item.meta['duitang']['msg']
            assert '年' in item.meta['duitang']['msg']

        source = DuitangSource('明日方舟 年', strict=False)
        items = list(source[:10])

        assert len(items) == 10
        for item in items:
            assert '明日方舟' in item.meta['duitang']['msg']
            assert '年' in item.meta['duitang']['msg']
