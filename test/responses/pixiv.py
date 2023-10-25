import os

from test.responses import resp_recorder
from waifuc.source import PixivSearchSource


@resp_recorder()
def pixiv_search_surtr():
    # noinspection PyTypeChecker
    source = PixivSearchSource(
        'アークナイツ (surtr OR スルト OR 史尔特尔)',
        refresh_token=os.environ['PIXIV_REFRESH_TOKEN'],
    )
    _ = list(source[:10])
