import os
import re
from typing import Iterator, Tuple, Union

from hbutils.system import urlsplit

from .web import WebDataSource
from ..utils import get_requests_session, srequest


def _extract_words(keyword):
    return list(filter(bool, re.split(r'[\W_]+', keyword)))


class DuitangSource(WebDataSource):
    def __init__(self, keyword: str, strict: bool = True, page_size: int = 100,
                 group_name: str = 'duitang', download_silent: bool = True):
        WebDataSource.__init__(self, group_name, get_requests_session(), download_silent)
        self.keyword = keyword
        self.words = set(_extract_words(keyword))
        self.page_size: int = page_size
        self.strict = strict

    def _check_title(self, title):
        if not self.strict:
            return True
        else:
            t_words = set(_extract_words(title))
            return len(t_words & self.words) == len(self.words)

    def _iter_data(self) -> Iterator[Tuple[Union[str, int], str, dict]]:
        offset = 0
        while True:
            resp = srequest(self.session, 'GET', 'https://www.duitang.com/napi/blog/list/by_search/', params={
                'kw': self.keyword,
                'start': str(offset),
                'limit': str(self.page_size),
            })
            resp.raise_for_status()

            raw = resp.json()
            if 'data' not in raw or 'object_list' not in raw['data']:
                break

            posts = raw['data']['object_list']
            if not posts:
                break

            for post in posts:
                if not self._check_title(post['msg']):
                    continue

                url = post['photo']['path']
                _, ext_name = os.path.splitext(urlsplit(url).filename)
                filename = f'{self.group_name}_{post["id"]}{ext_name}'
                meta = {
                    'duitang': post,
                    'group_id': f'{self.group_name}_{post["id"]}',
                    'filename': filename,
                }
                yield post['id'], url, meta

            offset += self.page_size
