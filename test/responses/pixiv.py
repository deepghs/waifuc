import os

from gchar.games.arknights import Character as ArknightsCharacter
from gchar.resources.pixiv import get_pixiv_keywords

from test.responses import resp_recorder
from waifuc.source import PixivSearchSource

ch_surtr = ArknightsCharacter.get('surtr')
ch_surtr_keywords = get_pixiv_keywords(ch_surtr)


@resp_recorder()
def pixiv_search_surtr():
    # noinspection PyTypeChecker
    source = PixivSearchSource(
        ch_surtr_keywords,
        refresh_token=os.environ['PIXIV_REFRESH_TOKEN'],
    )
    _ = list(source[:10])
