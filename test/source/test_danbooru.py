import pytest

from waifuc.source import DanbooruSource, SafebooruSource, ATFBooruSource, E621Source, E926Source


class TestSourceDanbooru:
    @pytest.mark.unittest
    def test_danbooru_source(self, danbooru):
        source = DanbooruSource(['1girl', 'solo'])
        items = list(source[:10])

        assert len(items) == 10
        for item in items:
            assert '1girl' in item.meta['tags']
            assert 'solo' in item.meta['tags']

        assert 'danbooru' in items[0].meta

    def test_safebooru_source(self, safebooru):
        source = SafebooruSource(['1girl', 'solo'])
        items = list(source[:10])

        assert len(items) == 10
        for item in items:
            assert '1girl' in item.meta['tags']
            assert 'solo' in item.meta['tags']

    def test_atfbooru(self, atfbooru):
        source = ATFBooruSource(['scathach_(fate)_(all)'])
        items = list(source[:10])
        assert len(items) == 9
        for item in items:
            assert 'scathach_(fate)_(all)' in item.meta['tags']

    def test_e621(self, e621_amiya, e621_surtr):
        source = E621Source(['amiya_(arknights)', 'solo'])
        items = list(source[:10])
        assert len(items) == 10
        for item in items:
            assert 'amiya_(arknights)' in item.meta['tags']
            assert 'solo' in item.meta['tags']

        source = E621Source(['surtr_(arknights)', 'solo'])
        items = list(source[:10])
        assert len(items) == 3
        for item in items:
            assert 'surtr_(arknights)' in item.meta['tags']
            assert 'solo' in item.meta['tags']

    def test_e926(self, e926_amiya, e926_surtr):
        source = E926Source(['amiya_(arknights)', 'solo'])
        items = list(source[:10])
        assert len(items) == 10
        for item in items:
            assert 'amiya_(arknights)' in item.meta['tags']
            assert 'solo' in item.meta['tags']

        source = E926Source(['surtr_(arknights)', 'solo'])
        items = list(source[:10])
        assert len(items) == 1
        for item in items:
            assert 'surtr_(arknights)' in item.meta['tags']
            assert 'solo' in item.meta['tags']
