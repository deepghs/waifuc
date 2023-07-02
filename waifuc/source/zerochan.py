import os
import warnings
from enum import Enum
from typing import Iterator, Union, List, Optional, Mapping, Tuple
from urllib.parse import quote_plus

from hbutils.system import urlsplit

from .web import WebDataSource
from ..utils import get_requests_session, srequest, get_task_names

try:
    from typing import Literal
except (ImportError, ModuleNotFoundError):
    from typing_extensions import Literal


class Sort(str, Enum):
    ID = 'id'
    FAV = 'fav'


class Time(str, Enum):
    ALL = '0'
    LAST_7000 = '1'
    LAST_15000 = '2'


class Dimension(str, Enum):
    LARGE = 'large'
    HUGE = 'huge'
    LANDSCAPE = 'landscape'
    PORTRAIT = 'portrait'
    SQUARE = 'square'


SelectTyping = Literal['medium', 'large', 'full']


class ZerochanSource(WebDataSource):
    __SITE__ = 'https://www.zerochan.net'

    def __init__(self, word: Union[str, List[str]], sort: Sort = Sort.FAV, time: Time = Time.ALL,
                 dimension: Optional[Dimension] = None, color: Optional[str] = None, strict: bool = False,
                 select: SelectTyping = 'large', group_name: str = 'zerochan', download_silent: bool = True,
                 user_agent=None):
        if user_agent:
            headers = {'User-Agent': user_agent}
        else:
            headers = {}
        WebDataSource.__init__(self, group_name, get_requests_session(headers=headers), download_silent)
        self.word = word
        self.sort = sort
        self.time = time
        self.dimension = dimension
        self.color = color
        self.strict = strict
        self.select = select

    @property
    def _base_url(self) -> str:
        if isinstance(self.word, str):
            return f'{self.__SITE__}/{quote_plus(self.word)}'
        elif isinstance(self.word, (list, tuple)):
            return f'{self.__SITE__}/{",".join(map(quote_plus, self.word))}'
        else:
            raise TypeError(f'Unknown type of word - {self.word!r}.')

    @property
    def _params(self) -> Mapping[str, str]:
        params = {
            'json': '1',
            's': self.sort.value,
            't': self.time.value,
        }
        if self.dimension is not None:
            params['d'] = self.dimension.value
        if self.color is not None:
            params['c'] = self.color
        if self.strict:
            params['strict'] = '1'

        return params

    @classmethod
    def _get_urls(cls, data):
        id_ = data['id']
        medium_url = data['thumbnail']
        prefix = quote_plus(data['tag'].replace(' ', '.'))
        large_urls = [f'https://s1.zerochan.net/{prefix}.600.{id_}.jpg']
        full_urls = [
            f"https://static.zerochan.net/{prefix}.full.{id_}{ext}"
            for ext in ['.jpg', '.png']
        ]

        return {'medium': medium_url, 'large': large_urls, 'full': full_urls}

    def _get_url(self, data):
        urls = self._get_urls(data)
        if self.select == 'full':
            url_fallbacks = [*urls['full'], *urls['large']]
        elif self.select == 'large':
            url_fallbacks = urls['large']
        else:
            url_fallbacks = []

        for url in url_fallbacks:
            resp = srequest(self.session, 'HEAD', url, raise_for_status=False)
            if resp.ok:
                return url
        else:
            return urls['medium']

    def _iter_data(self) -> Iterator[Tuple[Union[str, int], str, dict]]:
        page = 1
        while True:
            resp = srequest(self.session, 'GET', self._base_url,
                            params={**self._params, 'p': str(page), 'l': '200'},
                            raise_for_status=False)
            if resp.status_code in {403, 404}:
                warnings.warn(f'{resp!r} found at {resp.request.url}, {get_task_names()!r}, quit!')
                break
            resp.raise_for_status()

            json_ = resp.json()
            if 'items' in json_:
                items = json_['items']
                print(warnings.warn(f'{len(items)} item(s) found in {get_task_names()}.'))
                for data in items:
                    url = self._get_url(data)
                    _, ext_name = os.path.splitext(urlsplit(url).filename)
                    filename = f'{self.group_name}_{data["id"]}{ext_name}'
                    meta = {
                        'zerochan': {
                            **data,
                            'url': url,
                        },
                        'group_id': f'{self.group_name}_{data["id"]}',
                        'filename': filename,
                    }
                    yield data["id"], url, meta
            else:
                break

            page += 1
