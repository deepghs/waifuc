import pytest
import responses
from gchar.games.arknights import Character as ArknightsCharacter
from gchar.resources.pixiv import get_pixiv_keywords

from waifuc.source import PixivSearchSource


@pytest.fixture()
def ch_surtr():
    return ArknightsCharacter.get('surtr')


@pytest.fixture()
def ch_surtr_keywords(ch_surtr):
    return get_pixiv_keywords(ch_surtr)


@pytest.mark.unittest
class TestSourcePixiv:
    @responses.activate
    def test_pixiv_search(self, ch_surtr_keywords, pixiv_search_surtr):
        source = PixivSearchSource(ch_surtr_keywords, refresh_token='use your own refresh token')
        items = list(source[:10])

        assert len(items) == 10
