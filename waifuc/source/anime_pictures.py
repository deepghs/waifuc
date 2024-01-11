import os
from enum import Enum
from typing import Iterator, Tuple, Union, List, Literal

import cloudscraper
from hbutils.system import urlsplit
from pyquery import PyQuery as pq

from .web import WebDataSource, DynamicUAWebDataSource
from ..utils import get_requests_session, srequest


class OrderBy(str, Enum):
    STAR_DATE = "stars_date"
    DATE = "date"
    DATE_REVERS = "date_r"
    RATING = "rating"
    DOWNLOADS = "views"
    SIZE = "size"
    TAG_COUNT = "tag_num"


class Period(str, Enum):
    ANYTIME = "0"
    PAST_DAY = "3"
    PAST_WEEK = "1"
    PAST_MONTH = "2"
    PAST_6_MONTHS = "4"
    PAST_YEAR = "5"
    PAST_2_YEARS = "6"
    PAST_3_YEARS = "7"


class AnimePicturesSource(DynamicUAWebDataSource):
    __api_root__ = 'https://api.anime-pictures.net'
    __root__ = 'https://anime-pictures.net'

    def __init__(self, tags: List[str], tag_mode: Literal['or', 'and'] = 'and',
                 denied_tags: List[str] = None, denied_tag_mode: Literal['or', 'and'] = 'or',
                 order_by: OrderBy = OrderBy.RATING, period: Period = Period.ANYTIME,
                 select: Literal['thumbnail', 'preview', 'original'] = 'original',
                 group_name: str = 'anime_pictures', download_silent: bool = True, **kwargs):
        WebDataSource.__init__(
            self, group_name,
            get_requests_session(session=cloudscraper.create_scraper()),
            download_silent,
        )
        self.tags, self.tag_mode = tags, tag_mode
        self.denied_tags, self.denied_tag_mode = (denied_tags or []), denied_tag_mode
        self.tag_mode = tag_mode
        self.order_by = order_by
        self.period = period
        self.select = select
        self.kwargs = kwargs

    def _args(self):
        params = self._params(1)
        tag_text = params.get('search_tag') or ''
        denied_tag_text = params.get('denied_tags') or ''
        return [tag_text, denied_tag_text]

    def _params(self, page):
        params = {
            'order_by': self.order_by.value,
            'ldate': self.period.value,
            'lang': 'en',
            'page': str(page),
        }
        if self.tag_mode == 'and':
            params['search_tag'] = '&&'.join(self.tags)
        else:
            params['search_tag'] = '||'.join(self.tags)
        if self.denied_tags:
            if self.denied_tag_mode == 'and':
                params['denied_tags'] = '&&'.join(self.denied_tags)
            else:
                params['denied_tags'] = '||'.join(self.denied_tags)

        return {**params, **self.kwargs}

    def _get_url(self, post, resp):
        id_, md5 = post['id'], post['md5']
        if self.select == 'thumbnail':
            return f'https://cdn.anime-pictures.net/previews/{md5[:3]}/{md5}_bp.jpg'
        elif self.select == 'preview':
            return f'https://cdn.anime-pictures.net/previews/{md5[:3]}/{md5}_cp.jpg'
        elif self.select == 'original':
            return pq(resp.text)('#rating a.download_icon').attr('href')
        else:
            raise ValueError(f'Invalid image selection - {self.select!r}.')

    def _check_session(self) -> bool:
        resp = srequest(self.session, 'GET', f'{self.__api_root__}/api/v3/posts', params={
            'ldate': '0',
            'lang': 'en',
            'page': '0',
        }, raise_for_status=False)
        return resp.status_code // 100 == 2

    def _iter_data(self) -> Iterator[Tuple[Union[str, int], str, dict]]:
        page = 0
        while True:
            resp = srequest(self.session, 'GET', f'{self.__api_root__}/api/v3/posts', params=self._params(page))
            resp.raise_for_status()

            posts = resp.json()['posts']
            if not posts:
                break

            for post in posts:
                resp_page = srequest(self.session, 'GET', f'{self.__root__}/posts/{post["id"]}?lang=en')
                resp_page.raise_for_status()

                url = self._get_url(post, resp_page)
                tags = [item.text().replace(' ', '_') for item in pq(resp_page.text)('ul.tags li > a').items()]
                _, ext_name = os.path.splitext(urlsplit(url).filename)
                filename = f'{self.group_name}_{post["id"]}{ext_name}'
                meta = {
                    'anime_pictures': post,
                    'group_id': f'{self.group_name}_{post["id"]}',
                    'filename': filename,
                    'tags': {key: 1.0 for key in tags}
                }
                yield post['id'], url, meta

            page += 1
