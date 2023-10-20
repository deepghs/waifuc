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
        assert items[0].meta['tags'] == pytest.approx({
            '1girl': 1.0, 'bare_shoulders': 1.0, 'black_socks': 1.0, 'breasts': 1.0, 'brown_hair': 1.0,
            'fatal_fury': 1.0, 'hand_fan': 1.0, 'high_ponytail': 1.0, 'holding': 1.0, 'holding_fan': 1.0,
            'ichitaroh': 1.0, 'japanese_clothes': 1.0, 'looking_at_viewer': 1.0, 'pink_background': 1.0,
            'shiranui_mai': 1.0, 'smile': 1.0, 'socks': 1.0, 'solo': 1.0, 'standing': 1.0,
            'standing_on_one_leg': 1.0, 'the_king_of_fighters': 1.0
        })
        assert 'danbooru' in items[0].meta

    @responses.activate
    def test_safebooru_source(self, safebooru):
        source = SafebooruSource(['1girl', 'solo'])
        items = list(source[:10])

        assert len(items) == 10
