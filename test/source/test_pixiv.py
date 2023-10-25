import pytest
import responses

from waifuc.source import PixivSearchSource


@pytest.mark.unittest
class TestSourcePixiv:
    @responses.activate
    def test_pixiv_search(self, pixiv_search_surtr):
        source = PixivSearchSource(
            'アークナイツ (surtr OR スルト OR 史尔特尔)',
            refresh_token='use your own refresh token'
        )
        items = list(source[:10])

        assert len(items) == 10
