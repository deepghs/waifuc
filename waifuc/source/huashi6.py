import os
from functools import lru_cache
from typing import Iterator, Tuple, Union
from urllib.parse import quote_plus, urljoin

from hbutils.system import urlsplit

from .web import WebDataSource
from ..utils import get_requests_session, srequest


class Huashi6Source(WebDataSource):
    __img_site_url__ = 'https://img2.huashi6.com'

    def __init__(self, word: str,
                 group_name: str = 'huashi6', download_silent: bool = True):
        WebDataSource.__init__(self, group_name, get_requests_session(), download_silent)
        self.word = word

    @classmethod
    @lru_cache()
    def _get_img_site_url(cls):
        return cls.__img_site_url__

    def _iter_data(self) -> Iterator[Tuple[Union[str, int], str, dict]]:
        page = 1

        while True:
            resp = srequest(self.session, 'POST', "https://rt.huashi6.com/search/all", data={
                'word': self.word,
                'index': str(page),
            }, headers={
                "referrer": f"https://www.huashi6.com/search?searchText={quote_plus(self.word)}&p={page}",
            })
            raw = resp.json()['data']
            if 'works' not in raw or not raw['works']:
                break

            for post in raw['works']:
                url = urljoin(self._get_img_site_url(), post['coverImage']['path'])
                _, ext_name = os.path.splitext(urlsplit(url).filename)
                filename = f'{self.group_name}_{post["id"]}{ext_name}'
                meta = {
                    'huashi6': post,
                    'group_id': f'{self.group_name}_{post["id"]}',
                    'filename': filename,
                }
                yield post['id'], url, meta

            page += 1
