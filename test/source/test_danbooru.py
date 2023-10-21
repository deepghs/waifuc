import pytest
import responses

from waifuc.source import DanbooruSource, SafebooruSource


@pytest.mark.unittest
class TestSourceDanbooru:
    @responses.activate
    def test_danbooru_source(self, danbooru):
        source = DanbooruSource(['1girl', 'solo'])
        items = list(source[:10])

        assert len(items) == 10
        for item in items:
            assert '1girl' in item.meta['tags']
            assert 'solo' in item.meta['tags']

        assert items[0].meta['tags'] == pytest.approx({
            '1girl': 1.0, 'asymmetrical_legwear': 1.0, 'bandaged_leg': 1.0, 'bandages': 1.0, 'belt': 1.0,
            'belt_buckle': 1.0, 'black_belt': 1.0, 'black_cape': 1.0, 'black_choker': 1.0, 'black_gloves': 1.0,
            'black_headwear': 1.0, 'black_thighhighs': 1.0, 'breasts': 1.0, 'brown_hair': 1.0, 'buckle': 1.0,
            'cape': 1.0, 'choker': 1.0, 'closed_mouth': 1.0, 'collarbone': 1.0, 'commentary': 1.0, 'cowboy_shot': 1.0,
            'dimzreiz': 1.0, 'dress': 1.0, 'fingerless_gloves': 1.0, 'gloves': 1.0, 'hat': 1.0, 'highres': 1.0,
            'holding': 1.0, 'holding_staff': 1.0, 'kono_subarashii_sekai_ni_shukufuku_wo!': 1.0, 'long_sleeves': 1.0,
            'looking_at_viewer': 1.0, 'megumin': 1.0, 'red_dress': 1.0, 'red_eyes': 1.0, 'short_dress': 1.0,
            'short_hair': 1.0, 'short_hair_with_long_locks': 1.0, 'sidelocks': 1.0, 'simple_background': 1.0,
            'single_thighhigh': 1.0, 'small_breasts': 1.0, 'smile': 1.0, 'smug': 1.0, 'solo': 1.0, 'staff': 1.0,
            'standing': 1.0, 'thighhighs': 1.0, 'v-shaped_eyebrows': 1.0, 'white_background': 1.0, 'witch_hat': 1.0,
            'zettai_ryouiki': 1.0
        })
        assert 'danbooru' in items[0].meta

    @responses.activate
    def test_safebooru_source(self, safebooru):
        source = SafebooruSource(['1girl', 'solo'])
        items = list(source[:10])

        assert len(items) == 10
        for item in items:
            assert '1girl' in item.meta['tags']
            assert 'solo' in item.meta['tags']
