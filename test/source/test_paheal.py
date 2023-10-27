import pytest
import responses

from waifuc.source import PahealSource


@pytest.mark.unittest
class TestSourcePaheal:
    @responses.activate
    def test_paheal(self, paheal_surtr):
        source = PahealSource(['surtr', 'arknights'])
        items = list(source[:20])
        assert len(items) == 20

        for item in items:
            assert 'Arknights' in item.meta['tags']
            assert 'Surtr' in item.meta['tags']
