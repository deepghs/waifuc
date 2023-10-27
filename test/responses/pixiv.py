import os

from test.responses import resp_recorder
from waifuc.source import PixivSearchSource, PixivUserSource, PixivRankingSource


@resp_recorder()
def pixiv_search_surtr():
    # noinspection PyTypeChecker
    source = PixivSearchSource(
        'アークナイツ (surtr OR スルト OR 史尔特尔)',
        refresh_token=os.environ['PIXIV_REFRESH_TOKEN'],
    )
    _ = list(source[:10])


@resp_recorder()
def pixiv_search_surtr_original():
    # noinspection PyTypeChecker
    source = PixivSearchSource(
        'アークナイツ (surtr OR スルト OR 史尔特尔)',
        select='original',
        refresh_token=os.environ['PIXIV_REFRESH_TOKEN'],
    )
    _ = list(source[:10])


@resp_recorder()
def pixiv_user_2864095():
    # noinspection PyTypeChecker
    source = PixivUserSource(
        2864095,
        refresh_token=os.environ['PIXIV_REFRESH_TOKEN'],
    )
    _ = list(source[:20])


@resp_recorder()
def pixiv_user_2864095_original():
    # noinspection PyTypeChecker
    source = PixivUserSource(
        2864095, select='original',
        refresh_token=os.environ['PIXIV_REFRESH_TOKEN'],
    )
    _ = list(source[:20])


@resp_recorder()
def pixiv_ranking_day():
    source = PixivRankingSource(
        'day',
        refresh_token=os.environ['PIXIV_REFRESH_TOKEN'],
    )
    _ = list(source[:20])


@resp_recorder()
def pixiv_ranking_week_r18():
    source = PixivRankingSource(
        'week_r18',
        refresh_token=os.environ['PIXIV_REFRESH_TOKEN'],
    )
    _ = list(source[:20])
