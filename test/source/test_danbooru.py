import pytest
import responses

from waifuc.source import DanbooruSource, SafebooruSource, ATFBooruSource, E621Source


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
            '1girl': 1.0, 'armpits': 1.0, 'bare_shoulders': 1.0, 'breasts': 1.0, 'cleavage': 1.0, 'collarbone': 1.0,
            'commentary_request': 1.0, 'cosplay': 1.0, 'cowboy_shot': 1.0, 'groin': 1.0, 'hair_between_eyes': 1.0,
            'iowa_(kancolle)': 1.0, 'kantai_collection': 1.0, 'large_breasts': 1.0, 'looking_at_viewer': 1.0,
            'midriff': 1.0, 'navel': 1.0, 'sidelocks': 1.0, 'solo': 1.0, 'standing': 1.0,
            'taiki_shuttle_(umamusume)': 1.0, 'taiki_shuttle_(umamusume)_(cosplay)': 1.0, 'umamusume': 1.0,
            'yasume_yukito': 1.0
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

    @responses.activate
    def test_atfbooru(self, atfbooru):
        source = ATFBooruSource(['scathach_(fate)_(all)'])
        items = list(source[:10])
        assert len(items) == 9
        for item in items:
            assert 'scathach_(fate)_(all)' in item.meta['tags']

    @responses.activate
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
