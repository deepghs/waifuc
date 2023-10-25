import pytest
import responses

from waifuc.source import ZerochanSource


@pytest.mark.unittest
class TestSourceZerochan:
    @responses.activate
    def test_zerochan(self, zerochan_surtr):
        source = ZerochanSource('Surtr (Arknights)')
        items = list(source[:10])
        assert len(items) == 10
        for item in items:
            assert 'Surtr (Arknights)' in item.meta['zerochan']['tags']

    @responses.activate
    def test_zerochan_ful(self, zerochan_surtr_full):
        source = ZerochanSource('Surtr (Arknights)', select='full')
        items = list(source[:10])
        assert len(items) == 10
        for item in items:
            assert 'Surtr (Arknights)' in item.meta['zerochan']['tags']
            assert 'full' in item.meta['url']

    @responses.activate
    def test_zerochan_strict(self, zerochan_surtr_strict):
        source = ZerochanSource('Surtr (Arknights)', strict=True)
        items = list(source[:10])
        assert len(items) == 10
        for item in items:
            assert 'Surtr (Arknights)' in item.meta['zerochan']['tags']
            assert 'Surtr (Arknights)' == item.meta['zerochan']['tag']
