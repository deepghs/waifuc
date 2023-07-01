import os
import re
from typing import Iterator, Tuple, Union, List, Optional

from hbutils.system import urlsplit

from .web import WebDataSource, NoURL
from ..utils import get_requests_session, srequest


class YandeLikeSource(WebDataSource):
    def __init__(self, site_name: str, site_url: str,
                 tags: List[str], start_page: int = 1, min_size: Optional[int] = 800,
                 group_name: Optional[str] = None, download_silent: bool = True):
        WebDataSource.__init__(self, group_name or site_name, get_requests_session(), download_silent)
        self.site_name = site_name
        self.site_url = site_url
        self.start_page = start_page
        self.min_size = min_size
        self.tags: List[str] = tags

    def _select_url(self, data):
        if self.min_size is not None:
            url_names = [key for key in data.keys() if key.endswith('_url')]
            name_pairs = [
                *(
                    (name, f'{name[:-4]}_width', f'{name[:-4]}_height')
                    for name in url_names
                ),
                ('file_url', 'width', 'height'),
            ]

            f_url, f_width, f_height = None, None, None
            for url_name, width_name, height_name in name_pairs:
                if url_name in data and width_name in data and height_name in data:
                    url, width, height = data[url_name], data[width_name], data[height_name]
                    if width >= self.min_size and height >= self.min_size:
                        if f_url is None or width < f_width:
                            f_url, f_width, f_height = url, width, height

            if f_url is not None:
                return f_url

        if 'file_url' in data:
            return data['file_url']
        else:
            raise NoURL

    def _request(self, page):
        resp = srequest(self.session, 'GET', f'{self.site_url}/post.json', params={
            'tags': ' '.join(self.tags),
            'limit': '100',
            'page': str(page),
        })
        print(resp.request.url)
        print(resp.json())
        return resp

    def _get_data_from_raw(self, raw):
        return raw

    def _iter_data(self) -> Iterator[Tuple[Union[str, int], str, dict]]:
        page = self.start_page
        while True:
            resp = self._request(page)
            resp.raise_for_status()

            page_list = self._get_data_from_raw(resp.json())
            if not page_list:
                break

            for data in page_list:
                try:
                    url = self._select_url(data)
                except NoURL:
                    continue

                _, ext_name = os.path.splitext(urlsplit(url).filename)
                filename = f'{self.group_name}_{data["id"]}{ext_name}'
                meta = {
                    self.site_name: data,
                    'group_id': f'{self.group_name}_{data["id"]}',
                    'filename': filename,
                    'tags': {key: 1.0 for key in re.split(r'\s+', data['tags'])}
                }
                yield data["id"], url, meta

            page += 1


class YandeSource(YandeLikeSource):
    def __init__(self, tags: List[str], min_size: Optional[int] = 800,
                 group_name: str = 'yande', download_silent: bool = True):
        YandeLikeSource.__init__(self, 'yande', 'https://yande.re',
                                 tags, 1, min_size, group_name, download_silent)


class KonachanSource(YandeLikeSource):
    def __init__(self, tags: List[str], min_size: Optional[int] = 800,
                 group_name: str = 'konachan', download_silent: bool = True):
        YandeLikeSource.__init__(self, 'konachan', 'https://konachan.com',
                                 tags, 1, min_size, group_name, download_silent)


class KonachanNetSource(YandeLikeSource):
    def __init__(self, tags: List[str], min_size: Optional[int] = 800,
                 group_name: str = 'konachan_net', download_silent: bool = True):
        YandeLikeSource.__init__(self, 'konachan_net', 'https://konachan.net',
                                 tags, 1, min_size, group_name, download_silent)
