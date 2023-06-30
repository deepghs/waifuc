import os
import warnings
from enum import Enum
from typing import Iterator, Union, List, Optional, Mapping
from urllib.parse import quote_plus

from PIL import Image, UnidentifiedImageError
from hbutils.system import TemporaryDirectory, urlsplit

from .base import BaseDataSource
from ..model import ImageItem
from ..utils import get_requests_session, download_file

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


class ZerochanSource(BaseDataSource):
    __SITE__ = 'https://www.zerochan.net'

    def __init__(self, word: Union[str, List[str]], sort: Sort = Sort.FAV, time: Time = Time.ALL,
                 dimension: Optional[Dimension] = None, color: Optional[str] = None, strict: bool = False,
                 select: SelectTyping = 'large', group_name: Optional[str] = None, download_silent: bool = True):
        self.word = word
        self.sort = sort
        self.time = time
        self.dimension = dimension
        self.color = color
        self.strict = strict
        self.select = select
        self.group_name = group_name or 'zerochan'
        self.download_silent = download_silent
        self.session = get_requests_session()

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
            resp = self.session.head(url)
            if resp.ok:
                return url
        else:
            return urls['medium']

    def _iter(self) -> Iterator[ImageItem]:
        page = 1
        while True:
            resp = self.session.get(self._base_url, params={**self._params, 'p': str(page), 'l': '10'})
            if resp.status_code in {403, 404}:
                break
            resp.raise_for_status()

            json_ = resp.json()
            if 'items' in json_:
                items = json_['items']
                for data in items:
                    url = self._get_url(data)

                    with TemporaryDirectory() as td:
                        _, ext_name = os.path.splitext(urlsplit(url).filename)
                        filename = f'{self.group_name}_{data["id"]}{ext_name}'
                        td_file = os.path.join(td, filename)

                        try:
                            download_file(
                                url, td_file, desc=filename,
                                silent=self.download_silent, session=self.session
                            )
                            image = Image.open(td_file)
                            image.load()
                        except UnidentifiedImageError:
                            warnings.warn(f'Zerochan resource {data["id"]} unidentified as image, skipped.')
                            continue
                        except IOError as err:
                            warnings.warn(f'Skipped due to error: {err!r}')
                            continue

                    meta = {
                        'zerochan': {
                            **data,
                            'url': url,
                        },
                        'group_id': f'{self.group_name}_{data["id"]}',
                        'filename': filename,
                    }
                    yield ImageItem(image, meta)

            page += 1
