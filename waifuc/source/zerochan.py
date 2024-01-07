import json
import os
import warnings
from enum import Enum
from typing import Iterator, Union, List, Optional, Mapping, Tuple, Literal
from urllib.parse import quote_plus, urljoin

from hbutils.system import urlsplit

from .web import WebDataSource
from ..utils import get_requests_session, srequest


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
                 user_agent=None, username: Optional[str] = None, password: Optional[str] = None):
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

        self.username = username
        self._password = password
        self._is_authed = False

    def _args(self):
        return [self.word]

    def _auth(self):
        if not self._is_authed and self.username is not None:
            resp = self.session.post(
                'https://www.zerochan.net/login',
                data={
                    'ref': '/',
                    'name': self.username,
                    'password': self._password,
                    'login': 'Login'
                },
                headers={
                    'Referrer': "https://www.zerochan.net/login?ref=%2F",
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,'
                              'image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                follow_redirects=False,
            )
            if resp.status_code != 303:
                raise ConnectionError('Username or password wrong, failed to login to zerochan.net.')

            self._is_authed = True

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

    def _get_urls(self, data):
        id_ = data['id']
        resp = srequest(
            self.session, 'GET', f'https://www.zerochan.net/{id_}',
            params={'json': '1'},
        )
        json_data = resp.json()
        return [
            ('full', json_data['full']),
            ('large', json_data['large']),
            ('medium', json_data['medium']),
            ('small', json_data['small']),
        ]

    def _get_url(self, data):
        urls = self._get_urls(data)
        urls_dict = dict(urls)
        if urls_dict.get(self.select):
            return urls_dict[self.select]
        else:
            for i, (name, _) in enumerate(urls):
                if name == self.select:
                    idx = i
                    break
            else:
                raise ValueError(f'Unknown select: {self.select!r}')

            ls, gs = [], []
            for i, (name, v) in enumerate(urls):
                if i == idx or not v:
                    continue

                if i < idx:
                    ls.append((i, name, v))
                else:
                    gs.append((i, name, v))

            ls = sorted(ls, key=lambda x: -x[0])
            _, _, url = [*ls, *gs][0]
            return url

    def _iter_data(self) -> Iterator[Tuple[Union[str, int], str, dict]]:
        self._auth()
        page = 1
        while True:
            quit_ = False
            _base_url = self._base_url
            while True:
                resp = srequest(self.session, 'GET', _base_url,
                                params={**self._params, 'p': str(page), 'l': '200'},
                                follow_redirects=False, raise_for_status=False)
                if resp.status_code // 100 == 3:
                    _base_url = urljoin(_base_url, resp.headers['Location'])
                elif resp.status_code in {403, 404}:
                    quit_ = True
                    break
                else:
                    resp.raise_for_status()
                    break

            if quit_:
                break

            json_ = resp.json()
            if 'items' in json_:
                items = json_['items']
                for data in items:
                    try:
                        url = self._get_url(data)
                    except json.JSONDecodeError as err:
                        warnings.warn(f'API of {self.__SITE__} died again, skipped! Error: {err!r}')
                        continue

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
