import pytest

from waifuc.action import CCIPAction
from waifuc.source import LocalSource


@pytest.fixture()
def ccip_simple_source(ccip_simple):
    yield LocalSource(ccip_simple)


@pytest.fixture()
def ccip_mudrock_source(ccip_mudrock):
    yield LocalSource(ccip_mudrock)


@pytest.mark.unittest
class TestActionCCIP:
    def test_ccip_action(self, ccip_simple_source: LocalSource):
        items = list(ccip_simple_source.attach(CCIPAction()))

        assert len(items) == 25
        assert sorted([item.meta['filename'] for item in items]) == [
            '0bf58e0d7dc126d13cd9cb3221d78747c6b09687.jpg',
            '126a55b7cb41a864b13fd67f4db6acff60a0dc49.jpg',
            '13702c2bd02637c57307cfce70014a0183af6c57.jpg',
            '139d19fafd98074c77f460f5ce12f9561ed57dbc.jpg',
            '21e64a59fa072730fbbb29119bda99e4e8f10a12.jpg',
            '239661d088e21504a56221727b9df52ac1337f10.jpg',
            '33dd867e99223af582315b6cdf7e27fdc14b7380.jpg',
            '357860093ccc71e66db29a342331dc23a97fd352.jpg',
            '4f1a04d45e3f881890eae084b8076260cba3aa60.jpg',
            '5f1c79793bdda2dbcafdbb77f189ecd30a69cc2a.jpg',
            '7540e9466897865e8e5d48c8bbc34717830999cc.jpg',
            '7e6c9b3b83d0c1a648d92afccb62aee86def3cdd.jpg',
            '8a0321a2ce618d8d709800e8bea8c69b498dfe1a.jpg',
            '9e14004a78fb010d436666fa3b059b2fbf39697a.jpg',
            'ad4657a1a344172afc02dc6b7c2892e8da6d61cb.jpg',
            'ae1d9e9b3f9d4b76efbd24e58c33b371c8811935.jpg',
            'b0a69171147bc674e78411c4d0bd3da517256684.jpg',
            'bc2697e552c23a76ed766153f2206c7c45c12452.jpg',
            'c6dfddb751cc84cce447fb958b868ab2894aa1ef.jpg',
            'da7da945a7eae4d0bc7e2ff691e9f77e08b834de.jpg',
            'eb8dd992211f75f7bfa806ccaa25af37848a83ea.jpg',
            'ee01538f06f5b287a84098227af1fab6165bbff2.jpg',
            'ee995e16cf7c12a7a1d64d2f75ed28e3b3765780.jpg',
            'f36a85d478556ba918e3cc90c0fa869f3bed4e01.jpg',
            'f71c3b04d460e35976f2ba03d22b9d315cd9448c.jpg'
        ]

    def test_ccip_with_anchor(self, ccip_simple_source, ccip_mudrock_source):
        items = list(ccip_simple_source.attach(CCIPAction(init_source=ccip_mudrock_source)))

        assert len(items) == 12
        assert sorted([item.meta['filename'] for item in items]) == [
            '467c6ae2a4acaed4fa62ce70fba1b68c1734a192.jpg',
            '6ab8319ef0ee88bcbe2c5b7bede384aaa7ac1190.jpg',
            '817161b551092e83df40b449f92e210fbf1c4fa6.jpg',
            'a287f5284eb6e9b93efdb21535ca53a7f2fe10a7.jpg',
            'a89e144db45c8d8a11268226af13abfeb369dc43.jpg',
            'be2ae945bec0d05facafe19c098db51b805903c4.jpg',
            'ff2c422e361fc1e96cce01bfd9ca510f7255f149.jpg',
            'zerochan_3200855.jpg',
            'zerochan_3376023.jpg',
            'zerochan_3486072.jpg',
            'zerochan_3509457.jpg',
            'zerochan_3784336.jpg'
        ]
