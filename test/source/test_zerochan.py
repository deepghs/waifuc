import pytest

from waifuc.source import ZerochanSource


@pytest.mark.unittest
class TestSourceZerochan:

    def test_zerochan(self, zerochan_surtr):
        source = ZerochanSource('Surtr (Arknights)')
        items = list(source[:10])
        assert len(items) == 10
        for item in items:
            assert 'Surtr (Arknights)' in item.meta['zerochan']['tags']

    def test_zerochan_ful(self, zerochan_surtr_full):
        source = ZerochanSource('Surtr (Arknights)', select='full')
        items = list(source[:10])
        assert len(items) == 10
        for item in items:
            assert 'Surtr (Arknights)' in item.meta['zerochan']['tags']
            assert 'full' in item.meta['url']

    def test_zerochan_strict(self, zerochan_surtr_strict):
        source = ZerochanSource('Surtr (Arknights)', strict=True)
        items = list(source[:10])
        assert len(items) == 10
        for item in items:
            assert 'Surtr (Arknights)' in item.meta['zerochan']['tags']
            assert 'Surtr (Arknights)' == item.meta['zerochan']['tag']

    def test_zerochan_camilla(self, zerochan_camilla_strict):
        source = ZerochanSource('Camilla (Fire Emblem)', strict=True)
        items = list(source[:10])
        assert len(items) == 10
        for item in items:
            assert 'Camilla' in item.meta['zerochan']['tags']
            assert 'Camilla' in item.meta['zerochan']['tag']

    def test_zerochan_amiya_login(self, zerochan_amiya_login):
        source = ZerochanSource(
            'Amiya',
            username='your_username',
            password='your_password',
        )
        items = list(source[:10])
        assert len(items) == 10
        not_key = False
        for item in items:
            assert 'Amiya' in item.meta['zerochan']['tags']
            if 'Amiya' not in item.meta['zerochan']['tag']:
                not_key = True
        assert not_key

    def test_zerochan_amiya_login_strict(self, zerochan_amiya_login_strict):
        source = ZerochanSource(
            'Amiya',
            username='your_username',
            password='your_password',
            strict=True,
        )
        items = list(source[:10])
        assert len(items) == 10
        for item in items:
            assert 'Amiya' in item.meta['zerochan']['tags']
            assert 'Amiya' in item.meta['zerochan']['tag']
