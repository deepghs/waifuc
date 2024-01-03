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
            '1girl': 1.0, '2024': 1.0, 'absurdres': 1.0, 'arm_at_side': 1.0, 'armlet': 1.0, 'bangle': 1.0,
            'bare_shoulders': 1.0, 'black_hair': 1.0, 'blue_eyes': 1.0, 'blush': 1.0, 'bracelet': 1.0, 'breasts': 1.0,
            'china_dress': 1.0, 'chinese_clothes': 1.0, 'cleavage_cutout': 1.0, 'closed_mouth': 1.0,
            'clothing_cutout': 1.0, 'commentary_request': 1.0, 'dragon_print': 1.0, 'dress': 1.0, 'hand_up': 1.0,
            'happy_new_year': 1.0, 'highres': 1.0, 'jewelry': 1.0, 'knee_up': 1.0, 'large_breasts': 1.0, 'legs': 1.0,
            'light_smile': 1.0, 'long_hair': 1.0, 'looking_at_viewer': 1.0, 'navel': 1.0, 'navel_cutout': 1.0,
            'original': 1.0, 'oyaman': 1.0, 'panties': 1.0, 'pantyshot': 1.0, 'ponytail': 1.0, 'red_dress': 1.0,
            'red_footwear': 1.0, 'side_slit': 1.0, 'sideboob': 1.0, 'sleeveless': 1.0, 'sleeveless_dress': 1.0,
            'solo': 1.0, 'standing': 1.0, 'standing_on_one_leg': 1.0, 'thighs': 1.0, 'translation_request': 1.0,
            'twitter_username': 1.0, 'underwear': 1.0, 'white_panties': 1.0
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
