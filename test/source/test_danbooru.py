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

        with open('test_k.py', 'w') as f:
            print(items[0].meta['tags'], file=f)
        assert items[0].meta['tags'] == pytest.approx({
            '1girl': 1.0, 'absurdres': 1.0, 'bikini': 1.0, 'bird': 1.0, 'black_bikini': 1.0, 'breasts': 1.0,
            'curly_hair': 1.0, 'day': 1.0, 'eyewear_on_head': 1.0, 'floating': 1.0, 'floating_object': 1.0,
            'green_eyes': 1.0, 'green_hair': 1.0, 'hat': 1.0, 'highres': 1.0, 'karikarisuru': 1.0, 'ocean': 1.0,
            'one-punch_man': 1.0, 'sarong': 1.0, 'see-through_sarong': 1.0, 'side-tie_bikini_bottom': 1.0,
            'small_breasts': 1.0, 'solo': 1.0, 'straw_hat': 1.0, 'string_bikini': 1.0, 'sunglasses': 1.0,
            'swimsuit': 1.0, 'tatsumaki': 1.0, 'telekinesis': 1.0
        })
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
