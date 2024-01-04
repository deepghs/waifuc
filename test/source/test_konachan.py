import pytest

from waifuc.source import KonachanSource, KonachanNetSource, YandeSource, LolibooruSource, Rule34Source, HypnoHubSource, \
    GelbooruSource, XbooruSource, SafebooruOrgSource, TBIBSource


@pytest.mark.unittest
class TestSourceKonachan:
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

    def test_rule34(self, rule34_surtr, rule34_2dogs):
        source = Rule34Source(['surtr_(arknights)', 'solo'])
        items = list(source[:15])
        assert len(items) == 15
        for item in items:
            assert 'surtr_(arknights)' in item.meta['tags']
            assert 'solo' in item.meta['tags']

        source = Rule34Source(['texas_(arknights)', 'lappland_(arknights)', '2girls', '-comic', '-monochrome'])
        items = list(source[:20])
        assert len(items) == 20
        for item in items:
            assert 'texas_(arknights)' in item.meta['tags']
            assert 'lappland_(arknights)' in item.meta['tags']
            assert '2girls' in item.meta['tags']
            assert 'comic' not in item.meta['tags']
            assert 'monochrome' not in item.meta['tags']

    def test_hypnohub(self, hypnohub_surtr, hypnohub_2dogs):
        source = HypnoHubSource(['surtr_(arknights)'])
        items = list(source[:15])
        assert len(items) == 2
        for item in items:
            assert 'surtr_(arknights)' in item.meta['tags']

        source = HypnoHubSource(['texas_(arknights)', 'lappland_(arknights)'])
        items = list(source[:20])
        assert len(items) == 2
        for item in items:
            assert 'texas_(arknights)' in item.meta['tags']
            assert 'lappland_(arknights)' in item.meta['tags']

    def test_gelbooru(self, gelbooru_surtr, gelbooru_2dogs):
        source = GelbooruSource(['surtr_(arknights)', 'solo'])
        items = list(source[:15])
        assert len(items) == 15
        for item in items:
            assert 'surtr_(arknights)' in item.meta['tags']
            assert 'solo' in item.meta['tags']

        source = GelbooruSource(['texas_(arknights)', 'lappland_(arknights)', '2girls', '-comic', '-monochrome'])
        items = list(source[:20])
        assert len(items) == 20
        for item in items:
            assert 'texas_(arknights)' in item.meta['tags']
            assert 'lappland_(arknights)' in item.meta['tags']
            assert '2girls' in item.meta['tags']
            assert 'comic' not in item.meta['tags']
            assert 'monochrome' not in item.meta['tags']

    def test_xbooru(self, xbooru_surtr, xbooru_2dogs):
        source = XbooruSource(['surtr_(arknights)', 'solo'])
        items = list(source[:15])
        assert len(items) == 15
        for item in items:
            assert 'surtr_(arknights)' in item.meta['tags']
            # solo not in these tags in xbooru
            # assert 'solo' in item.meta['tags']

        source = XbooruSource(['texas_(arknights)', 'lappland_(arknights)', '2girls', '-comic', '-monochrome'])
        items = list(source[:20])
        assert len(items) == 8
        for item in items:
            assert 'texas_(arknights)' in item.meta['tags']
            assert 'lappland_(arknights)' in item.meta['tags']
            assert '2_girls' in item.meta['tags']
            assert 'comic' not in item.meta['tags']
            assert 'monochrome' not in item.meta['tags']

    def test_safebooru_org(self, safebooru_org_surtr, safebooru_org_2dogs):
        source = SafebooruOrgSource(['surtr_(arknights)', 'solo'])
        items = list(source[:15])
        assert len(items) == 15
        for item in items:
            assert 'surtr_(arknights)' in item.meta['tags']
            assert 'solo' in item.meta['tags']

        source = SafebooruOrgSource(['texas_(arknights)', 'lappland_(arknights)', '2girls', '-comic', '-monochrome'])
        items = list(source[:20])
        assert len(items) == 20
        for item in items:
            assert 'texas_(arknights)' in item.meta['tags']
            assert 'lappland_(arknights)' in item.meta['tags']
            assert '2girls' in item.meta['tags']
            assert 'comic' not in item.meta['tags']
            assert 'monochrome' not in item.meta['tags']

    def test_tbib(self, tbib_surtr, tbib_2dogs):
        source = TBIBSource(['surtr_(arknights)', 'solo'])
        items = list(source[:15])
        assert len(items) == 15
        for item in items:
            assert 'surtr_(arknights)' in item.meta['tags']
            assert 'solo' in item.meta['tags']

        source = TBIBSource(['texas_(arknights)', 'lappland_(arknights)', '2girls', '-comic', '-monochrome'])
        items = list(source[:20])
        assert len(items) == 20
        for item in items:
            assert 'texas_(arknights)' in item.meta['tags']
            assert 'lappland_(arknights)' in item.meta['tags']
            assert '2girls' in item.meta['tags']
            assert 'comic' not in item.meta['tags']
            assert 'monochrome' not in item.meta['tags']
