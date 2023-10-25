import os
from enum import IntFlag
from typing import Iterator, Tuple, Union, Optional, Literal

import cloudscraper
from hbutils.system import urlsplit

from .web import WebDataSource
from ..utils import get_requests_session, srequest


class Category(IntFlag):
    GENERAL = 0x4
    ANIME = 0x2
    PEOPLE = 0x1

    DEFAULT = GENERAL | ANIME
    ALL = GENERAL | ANIME | PEOPLE

    @property
    def mark(self) -> str:
        return f'{"1" if self & self.GENERAL else "0"}' \
               f'{"1" if self & self.ANIME else "0"}' \
               f'{"1" if self & self.PEOPLE else "0"}'


class Purity(IntFlag):
    SFW = 0x4
    SKETCHY = 0x2
    NSFW = 0x1

    DEFAULT = SFW | SKETCHY
    ALL = SFW | SKETCHY | NSFW

    @property
    def mark(self) -> str:
        return f'{"1" if self & self.SFW else "0"}' \
               f'{"1" if self & self.SKETCHY else "0"}' \
               f'{"1" if self & self.NSFW else "0"}'


SortingTyping = Literal['date_added', 'relevance', 'random', 'views', 'favorites', 'toplist']
SelectTyping = Literal['original', 'thumbnail']


class WallHavenSource(WebDataSource):
    def __init__(self, query: str, category: Category = Category.DEFAULT,
                 purity: Purity = Purity.DEFAULT, sorting: SortingTyping = 'relavance',
                 no_ai: bool = True, min_size: Tuple[int, int] = (1, 1),
                 select: SelectTyping = 'original', api_key: Optional[str] = None,
                 group_name: str = 'wallhaven', download_silent: bool = True):
        session = get_requests_session(session=cloudscraper.create_scraper())
        if api_key:
            session.headers.update({'X-API-Key': api_key})
        WebDataSource.__init__(self, group_name, session, download_silent)

        self.query = query
        self.category = category
        self.purity = purity
        self.sorting = sorting
        self.no_ai = no_ai
        self.min_size = min_size
        self.select = select

    def _select_url(self, data):
        if self.select == 'original':
            return data['path']
        elif self.select == 'thumbnail':
            return data['thumbs']['original']
        else:
            raise ValueError(f'Unknown image selection - {self.select!r}.')

    def _iter_data(self) -> Iterator[Tuple[Union[str, int], str, dict]]:
        page = 1
        while True:
            resp = srequest(self.session, 'GET', 'https://wallhaven.cc/api/v1/search', params={
                'q': self.query,
                'categories': self.category.mark,
                'purity': self.purity.mark,
                'sorting': self.sorting,
                'ai_art_filter': "1" if self.no_ai else "0",
                'atleast': f'{self.min_size[0]}x{self.min_size[1]}',
                'page': str(page),
            })
            raw = resp.json()
            if not raw or not raw['data']:
                break

            for data in raw['data']:
                url = self._select_url(data)

                _, ext_name = os.path.splitext(urlsplit(url).filename)
                filename = f'{self.group_name}_{data["id"]}{ext_name}'
                meta = {
                    'wallhaven': data,
                    'group_id': f'{self.group_name}_{data["id"]}',
                    'filename': filename,
                }
                yield data['id'], url, meta

            page += 1
