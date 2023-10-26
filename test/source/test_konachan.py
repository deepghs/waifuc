import pytest
import responses

from waifuc.source import KonachanSource, KonachanNetSource, YandeSource, LolibooruSource


@pytest.mark.unittest
class TestSourceKonachan:
    @responses.activate
    def test_konachan(self, konachan_surtr, konachan_2dogs):
        source = KonachanSource(['surtr_(arknights)'])
        items = list(source[:15])
        assert len(items) == 15
        for item in items:
            assert 'surtr_(arknights)' in item.meta['tags']

        source = KonachanSource(['texas_(arknights)', 'lappland_(arknights)', '2girls'])
        items = list(source[:20])
        assert len(items) == 20
        for item in items:
            assert 'texas_(arknights)' in item.meta['tags']
            assert 'lappland_(arknights)' in item.meta['tags']
            assert '2girls' in item.meta['tags']

    @responses.activate
    def test_konachan_net(self, konachan_net_surtr, konachan_net_2dogs):
        source = KonachanNetSource(['surtr_(arknights)'])
        items = list(source[:15])
        assert len(items) == 15
        for item in items:
            assert 'surtr_(arknights)' in item.meta['tags']

        source = KonachanNetSource(['texas_(arknights)', 'lappland_(arknights)', '2girls'])
        items = list(source[:20])
        assert len(items) == 20
        for item in items:
            assert 'texas_(arknights)' in item.meta['tags']
            assert 'lappland_(arknights)' in item.meta['tags']
            assert '2girls' in item.meta['tags']

    @responses.activate
    def test_yande(self, yande_surtr, yande_2dogs):
        source = YandeSource(['surtr_(arknights)'])
        items = list(source[:15])
        assert len(items) == 15
        for item in items:
            assert 'surtr_(arknights)' in item.meta['tags']

        source = YandeSource(['texas_(arknights)', 'lappland_(arknights)'])
        items = list(source[:20])
        assert len(items) == 20
        for item in items:
            assert 'texas_(arknights)' in item.meta['tags']
            assert 'lappland_(arknights)' in item.meta['tags']

    @responses.activate
    def test_lolibooru(self, lolibooru_surtr, lolibooru_2dogs):
        source = LolibooruSource(['surtr_(arknights)', 'solo'])
        items = list(source[:15])
        assert len(items) == 6
        for item in items:
            assert 'surtr_(arknights)' in item.meta['tags']
            assert 'solo' in item.meta['tags']

        source = LolibooruSource(['texas_(arknights)', 'lappland_(arknights)', '2girls', '-comic', '-monochrome'])
        items = list(source[:20])
        assert len(items) == 20
        for item in items:
            assert 'texas_(arknights)' in item.meta['tags']
            assert 'lappland_(arknights)' in item.meta['tags']
            assert '2girls' in item.meta['tags']
            assert 'comic' not in item.meta['tags']
            assert 'monochrome' not in item.meta['tags']
