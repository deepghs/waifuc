import os

import pytest
import responses

from waifuc.source import PixivSearchSource, PixivUserSource, PixivRankingSource


@pytest.mark.unittest
class TestSourcePixiv:
    @responses.activate
    def test_pixiv_search(self, pixiv_search_surtr, pixiv_search_surtr_original):
        source = PixivSearchSource(
            'アークナイツ (surtr OR スルト OR 史尔特尔)',
            refresh_token='use your own refresh token'
        )
        items = list(source[:10])
        assert len(items) == 10
        for item in items:
            assert os.path.splitext(item.meta['filename'])[1] == '.jpg'

        source = PixivSearchSource(
            'アークナイツ (surtr OR スルト OR 史尔特尔)',
            select='original',
            refresh_token='use your own refresh token'
        )
        items = list(source[:10])
        assert len(items) == 10
        for item in items:
            assert 'img-original' in item.meta['url']

    @responses.activate
    def test_pixiv_user(self, pixiv_user_2864095, pixiv_user_2864095_original):
        source = PixivUserSource(
            2864095,
            refresh_token='use your own refresh token'
        )
        items = list(source[:20])
        assert len(items) == 20
        for item in items:
            assert os.path.splitext(item.meta['filename'])[1] == '.jpg'

        source = PixivUserSource(
            2864095, select='original',
            refresh_token='use your own refresh token'
        )
        items = list(source[:20])
        assert len(items) == 20
        for item in items:
            assert 'img-original' in item.meta['url']

    @responses.activate
    def test_pixiv_ranking(self, pixiv_ranking_day, pixiv_ranking_week_r18):
        source = PixivRankingSource(
            'day',
            refresh_token='use your own refresh token'
        )
        items = list(source[:20])
        assert len(items) == 20
        for item in items:
            assert os.path.splitext(item.meta['filename'])[1] == '.jpg'

        source = PixivRankingSource(
            'week_r18',
            refresh_token='use your own refresh token'
        )
        items = list(source[:20])
        assert len(items) == 20
        for item in items:
            assert os.path.splitext(item.meta['filename'])[1] == '.jpg'
