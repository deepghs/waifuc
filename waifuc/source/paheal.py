import os
import re
from typing import Optional, List, Iterator, Tuple, Union

import xmltodict
from hbutils.system import urlsplit

from .web import WebDataSource, NoURL
from ..utils import get_requests_session, srequest


class PahealSource(WebDataSource):
    def __init__(self, tags: List[str], user_id: Optional[str] = None, api_key: Optional[str] = None,
                 min_size: Optional[int] = 800, download_silent: bool = True, group_name: str = 'paheal'):
        WebDataSource.__init__(self, group_name, get_requests_session(), download_silent)
        self.tags = tags
        self.min_size = min_size
        self.user_id, self.api_key = user_id, api_key

    def _params(self, page):
        params = {
            'tags': ' '.join(self.tags),
            'limit': '100',
            'page': str(page),
        }
        if self.user_id and self.api_key:
            params['user_id'] = self.user_id
            params['api_key'] = self.api_key

        return params

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
                    url, width, height = data[url_name], int(data[width_name]), int(data[height_name])
                    if width >= self.min_size and height >= self.min_size:
                        if f_url is None or width < f_width:
                            f_url, f_width, f_height = url, width, height

            if f_url is not None:
                return f_url

        if 'file_url' in data:
            return data['file_url']
        else:
            raise NoURL

    def _iter_data(self) -> Iterator[Tuple[Union[str, int], str, dict]]:
        page = 1
        while True:
            resp = srequest(self.session, 'GET', 'https://rule34.paheal.net/api/danbooru/find_posts/index.xml',
                            params=self._params(page))
            resp.raise_for_status()
            posts = xmltodict.parse(resp.text)['posts']['tag']

            for data in posts:
                data = {key.lstrip('@'): value for key, value in data.items()}

                try:
                    url = self._select_url(data)
                except NoURL:
                    continue

                _, ext_name = os.path.splitext(urlsplit(url).filename)
                filename = f'{self.group_name}_{data["id"]}{ext_name}'
                meta = {
                    'paheal': data,
                    'group_id': f'{self.group_name}_{data["id"]}',
                    'filename': filename,
                    'tags': {key: 1.0 for key in re.split(r'\s+', data['tags'])}
                }
                yield data["id"], url, meta

            page += 1
