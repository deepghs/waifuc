import pytest

from waifuc.source import LocalSource, EmptySource


@pytest.fixture()
def z5(zerochan_5):
    return LocalSource(zerochan_5)


@pytest.fixture()
def z20(zerochan_20):
    return LocalSource(zerochan_20)


@pytest.fixture()
def d5(danbooru_5):
    return LocalSource(danbooru_5)


@pytest.fixture()
def d20(danbooru_20):
    return LocalSource(danbooru_20)


@pytest.mark.unittest
class TestSourceCompose:
    def test_add_1(self, z20, d20):
        s = z20 + d20
        items = list(s)
        for item in items[:20]:
            assert item.meta['filename'].startswith('zerochan_')
        for item in items[20:]:
            assert item.meta['filename'].startswith('danbooru_')

    def test_add_2(self, z20, d20):
        s = d20 + z20
        items = list(s)
        for item in items[:20]:
            assert item.meta['filename'].startswith('danbooru_')
        for item in items[20:]:
            assert item.meta['filename'].startswith('zerochan_')

    def test_add_multiple(self, z5, d5, z20, d20):
        s = EmptySource() + z5 + (d5 + z20) + d20 + EmptySource()
        items = list(s)
        for item in items[:5]:
            assert item.meta['filename'].startswith('zerochan_')
        for item in items[5:10]:
            assert item.meta['filename'].startswith('danbooru_')
        for item in items[10:30]:
            assert item.meta['filename'].startswith('zerochan_')
        for item in items[30:]:
            assert item.meta['filename'].startswith('danbooru_')

    def test_parallel_1(self, z20, d20):
        s = z20 | d20
        items = list(s)
        assert not all(
            item.meta['filename'].startswith('zerochan_')
            for item in items[:20]
        ), 'The first 20 items should not be all zerochan.'
        assert not all(
            item.meta['filename'].startswith('danbooru_')
            for item in items[20:]
        ), 'The last 20 items should not be all danbooru'
