import os
from typing import Literal, Optional, Iterator, Tuple, Union, List

from hbutils.system import urlsplit

from .web import WebDataSource
from ..utils import get_requests_session, srequest

SelectTyping = Literal['thumb', 'small', 'medium', 'large', 'full']


class DerpibooruLikeSource(WebDataSource):
    def __init__(self, site_name: str, site_url: str,
                 tags: List[str], key: Optional[str] = None, select: SelectTyping = 'large',
                 download_silent: bool = True, group_name: Optional[str] = None):
        WebDataSource.__init__(self, group_name or site_name, get_requests_session(), download_silent)
        self.tags = tags
        self.key = key
        self.select = select
        self.site_name = site_name
        self.site_url = site_url

    def _params(self, page):
        params = {
            'q': ' '.join(self.tags),
            'per_page': '100',
            'page': str(page),
        }
        if self.key:
            params['key'] = self.key

        return params

    def _get_url(self, data):
        if self.select in data['representations']:
            return data['representations'][self.select]
        else:
            return data['representations']['full']

    def _iter_data(self) -> Iterator[Tuple[Union[str, int], str, dict]]:
        page = 1
        while True:
            resp = srequest(self.session, 'GET', f'{self.site_url}/api/v1/json/search/images',
                            params=self._params(page))
            resp.raise_for_status()

            posts = resp.json()['images']
            for data in posts:
                url = self._get_url(data)
                _, ext_name = os.path.splitext(urlsplit(url).filename)
                filename = f'{self.group_name}_{data["id"]}{ext_name}'
                meta = {
                    self.site_name: data,
                    'group_id': f'{self.group_name}_{data["id"]}',
                    'filename': filename,
                    'tags': {key.replace(' ', '_'): 1.0 for key in data['tags']}
                }
                yield data['id'], url, meta

            page += 1


class DerpibooruSource(DerpibooruLikeSource):
    def __init__(self, tags: List[str], key: Optional[str] = None, select: SelectTyping = 'large',
                 download_silent: bool = True, group_name: str = 'derpibooru'):
        DerpibooruLikeSource.__init__(self, 'derpibooru', 'https://derpibooru.org',
                                      tags, key, select, download_silent, group_name)


class FurbooruSource(DerpibooruLikeSource):
    def __init__(self, tags: List[str], key: Optional[str] = None, select: SelectTyping = 'large',
                 download_silent: bool = True, group_name: str = 'furbooru'):
        DerpibooruLikeSource.__init__(self, 'furbooru', 'https://furbooru.com',
                                      tags, key, select, download_silent, group_name)
